FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    libhdf5-serial-dev \
    libblas-dev \
    liblapack-dev
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory (with our python app) into the container
COPY model /app/model
COPY webapp /app/webapp

ENV PYTHONPATH="${PYTHONPATH}:/app"

# Define the command that will be executed when the docker is run
CMD ["python", "/app/webapp/app.py"]