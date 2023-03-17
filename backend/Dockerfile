FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
WORKDIR /app
COPY . /app
#CMD ["python", "endpoints.py"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "endpoints:app"]