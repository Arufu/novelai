FROM kykira/noval_ai

ENV WORKDIR=/app

COPY . $WORKDIR

RUN cd $WORKDIR

WORKDIR $WORKDIR

CMD ["./start.sh"]