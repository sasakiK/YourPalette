FROM python:3.6

RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi

RUN pip install uWSGI==2.0.8 \
                dash==0.21.1 \
                dash-renderer==0.12.1 \
                dash-html-components==0.10.1 \
                dash-core-components==0.22.1  \
                plotly \
                pandas
WORKDIR /app
COPY app /app
COPY cmd.sh /

USER uwsgi

EXPOSE 5000

CMD ["/cmd.sh"]
