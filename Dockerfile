FROM python:3.8.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /APIHUB


COPY . .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
RUN chmod +x ./start.sh





EXPOSE 8000


CMD ["./start.sh"]

