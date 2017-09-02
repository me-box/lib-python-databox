FROM phiwal/py3.5-tensorflow-opencv
MAINTAINER DataBox <p.yadav@acm.org>

ADD .  /app

WORKDIR /app

RUN echo "Hello User!"

RUN pip3 install -r ./requirements.txt

EXPOSE 8080

LABEL databox.type="driver"

ENTRYPOINT ["python3"]
CMD ["-u", "main.py" ]

#ENTRYPOINT ["/usr/bin/bash"]

#CMD ["-u", "facenet/src/2A.py" ]
