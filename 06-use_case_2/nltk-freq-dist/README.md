# README

## Building the Docker image
`docker build -t nltk-freq-dist .`

## Running the Docker image
Change to the directory where you have a folder containing input (a list of *.txt files), and a folder that can be used for writing results.  Let's say that I have this under /Users/jon/test-data:

`cd /Users/jon/test-data`

If I have an input folder named "input" an and output folder named "output", I can run the code through the container using the following command:

`docker run -it --rm -v "$PWD":/tmp --name nltk-freq-dist-instance nltk-freq-dist input output`

## Other Docker commands
Verify that the image was created locally

`docker images`


Remove the image (will warn you if you have running instances)

`docker rmi nltk-bow`