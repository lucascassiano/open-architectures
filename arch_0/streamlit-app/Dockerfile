# # a little overkill but need it to install dot cli for dtreeviz
# FROM ubuntu:20.04

# # ubuntu installing - python, pip, graphviz, nano, libpq (for psycopg2)
# RUN apt-get update &&\
#     apt-get install python3.7 -y &&\
#     apt-get install python3-pip -y &&\
#     apt-get install graphviz -y

FROM python:3.6

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

COPY . .


# --------------- Configure Streamlit ---------------
RUN mkdir -p /root/.streamlit
COPY ./.streamlit/config.toml /root/.streamlit
# RUN bash -c 'echo -e "\
# 	[server]\n\
#     enableXsrfProtection = false\n\
# 	enableCORS = false\n\
# 	" > /root/.streamlit/config.toml'


# --------------- Export envirennement variable ---------------
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV GIT_PYTHON_REFRESH=quiet

CMD [ "streamlit run", "./main.py" ]