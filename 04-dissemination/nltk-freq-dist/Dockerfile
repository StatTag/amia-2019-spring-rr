FROM python:2.7.16-alpine

LABEL=1.0.0

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader punkt

ENTRYPOINT [ "./run.sh" ]