# README

## Building the Docker image
`docker build -t nltk-freq-dist .`

Verify that the image was created locally.

`docker images`

If you need to remove the image the following command will remove the image locally.

`docker rmi nltk-freq-dist`

## Running the Docker image
Change to the directory where you have a folder containing input (a list of *.txt files), and a folder that can be used for writing results.  Let's say that I have this under /Users/jon/test-data:

`cd /Users/jon/test-data`

In my `test-data` folder, we have an input folder named "input" an and output folder named "output". I can run the code through the container using the following command:

`docker run --rm -v "$PWD":/tmp nltk-freq-dist input output`

Here the `-v "$PWD":/tmp` option is telling Docker to map the current directory on our machine (the directory we're in, which Docker discovers via `"$PWD"`) to the `/tmp` directory in the container.  Within the container, it can access `/tmp/input` to get to all of our text files, and it can write results to `/tmp/output`.  When the container stops running, the files in the input and output directory still exist.

## Input files
The program expects a single directory (no nested folders) of .txt files.  Each file can represent a single document for a single patient, or can combine all of the documents for a patient into the same file.  The file name will be used as the unique key for the results in the output

## Output files
The program creates a file named `results.csv` which will contain the top 50 term frequencies for each document.  The format is:

`file_id,term,count`