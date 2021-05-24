FROM python:3.7.3
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
COPY /thread_fetcher /app
WORKDIR app
CMD ["python3", "./main.py"]