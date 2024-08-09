FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
RUN python /app/manage.py collectstatic
RUN mkdir /app/sqlite
RUN mkdir /app/media
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi"]
