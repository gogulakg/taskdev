FROM python:2.7.18

ADD .env .
ADD app.py .
ADD requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8080

CMD [ "python", "./app.py" ]