from celery import Celery


broker_url = "amqp://guest:guest@rabbitmq:5672"
app = Celery(broker=broker_url)


@app.task
def hello() -> str:
    return "Hello world!"
