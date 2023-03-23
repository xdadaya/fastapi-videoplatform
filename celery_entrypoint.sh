#!/bin/sh

celery -A app.celery.app worker -l info

exec "$@"