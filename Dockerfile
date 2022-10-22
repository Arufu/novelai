FROM python:alpine

ENV WORKDIR=/app

COPY ./requirements.txt $WORKDIR/requirements.txt

RUN apk update
RUN apk add build-base

RUN cd $WORKDIR && \
    pip install --upgrade pip >/dev/null 2>&1
RUN pip install -r $WORKDIR/requirements.txt

WORKDIR $WORKDIR

CMD ["./start.sh"]