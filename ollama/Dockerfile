FROM ollama/ollama

ENV APP_HOME=/home

WORKDIR $APP_HOME

COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["bash", "entrypoint.sh"]