FROM python:alpine

ENV WORKDIR=/app

COPY ./requirements.txt $WORKDIR/requirements.txt

RUN apk add --update --no-cache postgresql-client jpeg-dev &&\
    apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev \

RUN cd $WORKDIR && \
    pip install --upgrade pip &&\
    pip install -r requirements.txt

WORKDIR /app

CMD ["./start.sh"]