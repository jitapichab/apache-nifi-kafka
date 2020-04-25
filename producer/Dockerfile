FROM python:alpine

WORKDIR /app
ADD app .


ADD  requirements.txt .

RUN  pip install -r requirements.txt

CMD [ "python", "main.py" ]
