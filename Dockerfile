FROM python:3.8

ADD . /opt

WORKDIR /opt

RUN pip3 install -r requirements.txt

CMD ["python3", "flask_app.py"]