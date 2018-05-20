FROM python:3.5-alpine
MAINTAINER DataBox <p.yadav@acm.org>

ADD . ./pydriver

WORKDIR /pydriver

RUN apk add --update bash && apk add libxtst-dev &&  apk add gcc && apk add vim && rm -rf /var/cache/apk/*

ENV PYZMQ_VERSION="==16.0.2"
ENV ZEROMQ_VERSION="4.2.2"

RUN apk add --no-cache python python-dev build-base git libtool pkgconfig autoconf automake wget ca-certificates && \
    wget "https://bootstrap.pypa.io/get-pip.py" -O /dev/stdout | python && \
    pip install pyzmq${PYZMQ_VERSION} && \
    cd /tmp && \
    wget https://github.com/zeromq/libzmq/releases/download/v${ZEROMQ_VERSION}/zeromq-${ZEROMQ_VERSION}.tar.gz && \
    tar -xzf zeromq-${ZEROMQ_VERSION}.tar.gz && \
    cd zeromq-${ZEROMQ_VERSION} && \
    ./autogen.sh && ./configure && make && make install && \
    rm -rf /tmp/zeromq-${ZEROMQ_VERSION}* && rm -rf /tmp/* && \
    apk del python-dev build-base git libtool pkgconfig autoconf automake wget ca-certificates && \
    apk add --no-cache libstdc++

RUN pip install -r ./requirements.txt

RUN echo "Hello User!"

EXPOSE 8080

LABEL databox.type="driver"

ENTRYPOINT ["python"]

CMD ["-u", "main.py" ]
