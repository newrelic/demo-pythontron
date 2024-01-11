FROM python:3.7

RUN apt-get clean all
RUN apt-get update
RUN apt update
RUN apt -y install wget curl

RUN mkdir /mnt/pythontron
COPY ./python/requirements.txt ./python/linux-requirements.txt /mnt/pythontron/

WORKDIR /mnt/pythontron

COPY ./python /mnt/pythontron/
# RUN python3 -m pip install --no-cache-dir dependency-injector
RUN python3 -m pip install --no-cache-dir -r requirements.txt -r linux-requirements.txt --user
EXPOSE 3001
CMD ["python3", "tron.py", "-c", "config/app_config.json"]
