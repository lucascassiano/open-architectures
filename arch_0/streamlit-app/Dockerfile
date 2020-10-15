# a little overkill but need it to install dot cli for dtreeviz
FROM ubuntu:20.04

# ubuntu installing - python, pip, graphviz, nano, libpq (for psycopg2)
RUN apt-get update &&\
    apt-get install python3.7 -y &&\
    apt-get install python3-pip -y &&\
    apt-get install graphviz -y

# FROM python:3.6-slim

WORKDIR /usr/src/app

# # RUN pip install urllib3
# RUN pip install --no-cache-dir matplotlib pandas

# RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
# RUN apk --no-cache --update-cache add gcc gfortran build-base wget freetype-dev libpng-dev openblas-dev
# RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
# RUN hostnamectl
# required for Numpy
# RUN apt-get update
# RUN apt-get install -y software-properties-common \
#     apt-add-repository universe \ 
#     apt-get update \
#     apt-get install python-pip

# RUN apk add --no-cache python3-dev libstdc++ && \
#     apk add --no-cache g++ && \
#     ln -s /usr/include/locale.h /usr/include/xlocale.h && \
#     pip3 install numpy && \
#     pip3 install pandas

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install -r requirements.txt

COPY . .

# streamlit-specific commands for config
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'

RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
" > /root/.streamlit/config.toml'

CMD [ "streamlit run", "./main.py" ]