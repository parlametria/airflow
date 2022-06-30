FROM python:3.8.10-slim-buster

#RUN apt-get update && apt-get install curl python-requests -y
#RUN curl -sSL https://install.python-poetry.org | python -

#ENV PATH /root/.local/bin:$PATH
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /atualiza_parlamentares
COPY . /atualiza_parlamentares

#RUN poetry install
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -e .

#ENTRYPOINT ["/atualiza_parlamentares/run.sh"]
