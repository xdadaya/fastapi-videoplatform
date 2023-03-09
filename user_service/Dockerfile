FROM public.ecr.aws/docker/library/python:3.11
RUN apt-get update && apt-get install -y dos2unix
WORKDIR /app/user_service/

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./user_service .
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy


COPY user_service_entrypoint.sh /user_service_entrypoint.sh
RUN chmod a+x /user_service_entrypoint.sh
RUN dos2unix /user_service_entrypoint.sh && apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/*