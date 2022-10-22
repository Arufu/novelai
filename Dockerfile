FROM python:alpine

ENV WORKDIR=/app

COPY . $WORKDIR

RUN cd $WORKDIR && \
    pip install --upgrade pip &&\
    pip install -r requirements.txt

WORKDIR /app

CMD ["./start.sh"]