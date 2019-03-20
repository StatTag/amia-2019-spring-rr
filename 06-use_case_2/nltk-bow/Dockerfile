FROM python:2

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader punkt

COPY . .

CMD [ "python", "./bow.py" ]