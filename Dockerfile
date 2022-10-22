FROM python:alpine

ENV WORKDIR=/app

COPY ./requirements.txt $WORKDIR/requirements.txt

RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN cd $WORKDIR && \
    pip install --upgrade pip >/dev/null 2>&1 &&\
    pip install -r requirements.txt

WORKDIR /app

CMD ["./start.sh"]