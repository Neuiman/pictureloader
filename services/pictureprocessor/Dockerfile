FROM python:3.12.6

RUN mkdir /pictureprocessor

WORKDIR /pictureprocessor


COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x scripts/*.sh

CMD ["/bin/bash", "/pictureprocessor/scripts/start.sh"]

