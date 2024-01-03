FROM python:3.11
WORKDIR /
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt
COPY app app
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "app.main:app", "--reload", "--reload-dir", "/app"]
