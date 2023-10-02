FROM python:3.8-slim

MAINTAINER Martin Beisel "martin.beisel@iaas.uni-stuttgart.de"

# configure installs to run non interactive
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install gnupg -y
RUN apt-get install ca-certificates -y

# install tzdata with a default timezone
ENV TZ=Europe/Berlin
RUN apt-get install tzdata

# install texlive
RUN apt-get install texlive texlive-latex-extra texlive-luatex texlive-xetex texlive-lang-european -y

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN apt-get update
RUN apt-get install -y gcc python3-dev
RUN pip install -r requirements.txt
COPY . /app

ENTRYPOINT [ "python" ]

CMD ["app.py" ]