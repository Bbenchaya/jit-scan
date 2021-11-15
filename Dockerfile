FROM python:3.8-slim-buster

WORKDIR /app


#Install Git
RUN apt-get -y update
RUN apt-get -y install git

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN mkdir /repositories_to_inspect

COPY . .

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]