FROM python:3.12.6

RUN mkdir /web

WORKDIR /web

COPY requirements.txt .

RUN pip install -r requirements.txt

Copy . .

RUN chmod a+x scripts/*.sh

CMD ["/bin/bash", "/web/scripts/start.sh"]