M python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 10149
CMD ["gunicorn", "--bind", "0.0.0.0:10149", "app:app"]

