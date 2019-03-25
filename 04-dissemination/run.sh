cd test-data
docker run --rm -v "$PWD":/tmp nltk-freq-dist input output
cd ..