# FROM python:3.7.4-alpine3.10
FROM python:3.7
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV APP_HOME=/freightcrate
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static


# Set the working directory to /freightcrate
WORKDIR $APP_HOME

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

RUN ["chmod", "+x", "start.sh"]

CMD ["bash", "start.sh"]

# RUN chmod 777 run_test.sh

#create .env file

EXPOSE 8000
