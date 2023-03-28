FROM public.ecr.aws/docker/library/python:3.11
RUN apt-get update && apt-get install -y dos2unix
WORKDIR /app/statistics_service/

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./statistics_service .
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy


COPY statistics_service_entrypoint.sh /statistics_service_entrypoint.sh
COPY consumer_entrypoint.sh /consumer_entrypoint.sh
RUN chmod a+x /statistics_service_entrypoint.sh /consumer_entrypoint.sh
RUN dos2unix /statistics_service_entrypoint.sh /consumer_entrypoint.sh && apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/*