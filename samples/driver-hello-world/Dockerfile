FROM python:3.5-alpine
MAINTAINER DataBox <p.yadav@acm.org>

ADD . ./pydriver

WORKDIR /pydriver

RUN pip install -r ./requirements.txt

RUN apk add --update bash && apk add libxtst-dev &&  apk add vim && rm -rf /var/cache/apk/*

RUN echo "Hello User!"

EXPOSE 8080

LABEL databox.type="driver"

ENTRYPOINT ["python"]

CMD ["-u", "main.py" ]
