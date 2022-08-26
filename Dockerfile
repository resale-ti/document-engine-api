FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p /app

WORKDIR /app

RUN apt-get update && apt-get upgrade -y &&  \
    apt-get install -y python3-dev locales && \
    sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

RUN pip install --upgrade pip

COPY requirements.txt /app

RUN pip install -r /app/requirements.txt 

ADD ./app /app