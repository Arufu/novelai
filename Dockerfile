FROM python:alpine

ENV WORKDIR=/app

COPY ./requirements.txt $WORKDIR/requirements.txt

RUN apk update
RUN apk add alpine-sdk rust cargo make ruby libressl-dev

RUN cd $WORKDIR && \
    pip install --upgrade pip >/dev/null 2>&1
RUN pip install -r $WORKDIR/requirements.txt

WORKDIR $WORKDIR

CMD ["./start.sh"]