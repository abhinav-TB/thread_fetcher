FROM python:3.7-alpine

ENV API_Key = "hPQHz3FXD5mWaahbws0wWiZNw"
ENV API_Secret_Key = "gX2TVu4hNXiUV9hrYEH8h2IUsNSsngkj1BMwxl4kqQ9IDUHB05"
ENV Bearer_Token = "AAAAAAAAAAAAAAAAAAAAAHdWPwEAAAAAzdTEolPrq6BeobItPwgpVv96cpc%3DOclZz6MoE84oadTxECxGcxdeHwjqjSMGyuPlxuovBDMHIFMLsd"
ENV Access_Token = "1395275310250160130-11m0HnsQGqUH9sIH9xNNIk0hV9fa6O"
ENV Access_Token_Secret = "HsmCNMKyiiJ7PYizRRjjfYdCPJNYSZtTexxlxsHmaFvP9"
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /thread_fetcher
CMD ["python3", "main.py"]