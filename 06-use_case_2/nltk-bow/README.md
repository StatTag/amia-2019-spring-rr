# README

## Building the Docker image
`docker build -t nltk-bow .`

## Running the Docker image
`docker run -it --rm --name nltk-bow-instance nltk-bow`

## Other Docker commands
Verify that the image was created locally

`docker images`


Remove the image (will warn you if you have running instances)

`docker rmi nltk-bow`