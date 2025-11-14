FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5050

# CMD ["python", "app.py"]

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5050", "app:app"]