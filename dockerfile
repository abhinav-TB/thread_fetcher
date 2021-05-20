FROM python:3.7
COPY requirements.txt /tmp
COPY /thread_fetcher /app
RUN pip install -r /tmp/requirements.txt

WORKDIR app
CMD ["python3", "./main.py"]