FROM python:3
MAINTAINER DataBox <p.yadav@acm.org>

ADD . ./pydriver

WORKDIR /pydriver

RUN pip install -r ./requirements.txt

EXPOSE 8080

LABEL databox.type="driver"

ENTRYPOINT ["python"]

CMD ["-u", "main.py" ]