# NOTE: this is for demo purposes ONLY. The implementation takes liberties with 
#      both value sets AND logic, so do NOT assume this is "correct"
#      We're mainly using this to show data prep

# OBJECTIVE: Implement the Northwestern Type 2 Diabetes Mellitus phenotype
# LOGIC SOURCE: 
#           https://phekb.org/phenotype/type-2-diabetes-mellitus
# PATIENT DATA SOURCE: 
#           We used Synthea (https://github.com/synthetichealth/synthea)
#           to generate 1,000 synethic patients
# WARNING: The implementation information is no longer available online
#           The site (NU VAULT) which housed it was retired. We obtained the implementation
#           PDF and extracted the relevant value sets MANUALLY
#           We then added additional codes where required based on our source data (from Synthea)
#           as Synthea uses SNOMED CT for condition information whereas the supplied phenotype
#           uses ICD-9 (it's from 2012). Given that, we also then had to MAP between ICD-9
#           and SNOMED CT using UMLS.

import random
import numpy
import pandas

# our source patient dx data is coded in SNOMED CT, but our system needs ICD-9
# we're going to use the UMLS ICD-9 to SNOMED CT maps + our source ICD-9 dx maps
# to create a new data set that says "patient has dx of type 1 or type 2 diabetes"
# we're going to represent this as a simple True/False (present, not present) indicator

# Let's get our map data
# obtain the map file from https://www.nlm.nih.gov/research/umls/mapping_projects/icd9cm_to_snomedct.html
# we want to focus on the following columns
# ICD_CODE - ICD-9-CM code
# SNOMED_CID - SNOMED CT concept identifier, the target of the map (null for ICD-9-CM codes without a map)
# we're only going to retain those two columns
dx_map = pandas.read_csv(
        'ICD9CM_TO_SNOMEDCT_DIAGNOSIS_201812/ICD9CM_SNOMED_MAP_1TOM_201812.txt'
        ,sep='\t'
        ,usecols=['ICD_CODE','SNOMED_CID']
        , dtype={'ICD_CODE': str, 'SNOMED_CID': str}
        #,index_col='ICD_CODE'
        #,index_col='SNOMED_CID'
        )

# in the event SNOMED_CID is null/NaN, we don't want that (no map)
dx_map = dx_map[dx_map['SNOMED_CID'].notnull()]

# take a look
#print dx_map
#print dx_map.keys()

# we're going to pull the term list from our algorithm
# this contains our list of known code (patterns) for general buckets of
# concepts used by portions of the logic
term_list = pandas.read_csv(
        'phenotype/algorithm_term_list.csv'
        , dtype={'code': str}
        )

# for "simplicity," we're going to blow out the list of valid dx codes by taking our
# ICD-9 to SNOMED CT map, then by algorithm bucket, creating distinct lists of ICD-9 to 
# SNOMED CT subsets for each portion of our algorithm
# ex:
#   algorithm 1:
#     - type 1
#     - type 2 (inclusion - temporary)
#     - type 2 (exclusion - temporary)
#     - type 2 (final list [inclusion - exclusion])
#   algorithm 8:
#     - (list)

# these are the list of patterns we want to focus on
term_list_dx_1_dm_type_1 = term_list[(term_list['algorithm'] == '1') & (term_list['domain'] =='dx' ) & (term_list['group'] =='dm_type_1' ) & (term_list['code_system'] =='ICD-9' ) & (term_list['include'] ==1 )]
term_list_dx_1_dm_type_2_include = term_list[(term_list['algorithm'] == '1') & (term_list['domain'] =='dx' ) & (term_list['group'] =='dm_type_2' ) & (term_list['code_system'] =='ICD-9' ) & (term_list['include'] ==1 )]
term_list_dx_1_dm_type_2_exclude = term_list[(term_list['algorithm'] == '1') & (term_list['domain'] =='dx' ) & (term_list['group'] =='dm_type_2' ) & (term_list['code_system'] =='ICD-9' ) & (term_list['exclude'] ==1 )]
term_list_dx_8 = term_list[(term_list['algorithm'] == '8') & (term_list['domain'] =='dx' ) & (term_list['group'] =='dm' ) & (term_list['code_system'] =='ICD-9' ) & (term_list['include'] ==1 )]

# note re: filtering a daraframe
# "~" negates the condition
# ex:   df[~df['some_col'].str.contains("some_pattern")]
#      find me rows where 'some_col' does NOT contain "some_pattern"
# filter out NaN with "na = False"

## some helper functions tp help us manipulate our dx concept data a bit

#take an ICD-style code and turn it into regex pattern group
def convertCodeEntryToRegex(str):
  #input: 230.x -> (230\\..)
  return '('+str.replace('.','\\.').replace('x','.')+')'
  #return '('+str.replace('.','\\.').replace('x','.*')+')'

#for each member of a dx column in a dataframe, join them into one single regex pattern
def convertDFColumnToRegex(df, colname):
  # we want to emit something like '(250\\..1)|(250\\..3)'
  aList = df[colname].apply(''.join).tolist()
  regexString = '|'.join(map(convertCodeEntryToRegex, aList))
  return regexString

#using the above functions, take two lists - one our UMLS ICD-9 to SNOMED map and the other our allowed
# list of ICD-9 codes - construct a regex to find the allowed codes and emit them (ICD-9, SNOMED CT)
def getDXCodesFromMap(dx_df, term_list_df):
  dx_match = convertDFColumnToRegex(term_list_df, 'code')
  #print dx_match
  dx_term_match = dx_df[dx_df.ICD_CODE.str.contains(dx_match)]
  return dx_term_match

# now let's blow out our ICD-9 to SNOMED map for each of these

########## Algorithm 1 -> DX list
dx_1_dm_type_1 = getDXCodesFromMap(dx_map, term_list_dx_1_dm_type_1)
dx_1_dm_type_1.set_index('SNOMED_CID')

########## Algorithm 2 -> DX list
## get our included codes
dx_1_dm_type_2_include = getDXCodesFromMap(dx_map, term_list_dx_1_dm_type_2_include)
## get our excluded codes (250.12, etc.)
dx_1_dm_type_2_exclude = getDXCodesFromMap(dx_map, term_list_dx_1_dm_type_2_exclude)
#remove the exclusion codes from the included codes - give us our final list
#note we need to remove the "null" rows from the initial inclusion set after the filter
dx_1_dm_type_2 = dx_1_dm_type_2_include[~dx_1_dm_type_2_include.isin(dx_1_dm_type_2_exclude)].dropna()
dx_1_dm_type_2.set_index('SNOMED_CID')

########## Algorithm 8 -> DX list
dx_8_dm = getDXCodesFromMap(dx_map, term_list_dx_8)
dx_8_dm.set_index('SNOMED_CID')

# if you want to review before we remove the columns, output them
dx_1_dm_type_1.to_csv('phenotype/generated/terms_dx_1_dm_type_1.csv', sep=',')
dx_1_dm_type_2.to_csv('phenotype/generated/terms_dx_1_dm_type_2.csv', sep=',')
dx_8_dm.to_csv('phenotype/generated/terms_dx_8_dm.csv', sep=',')
