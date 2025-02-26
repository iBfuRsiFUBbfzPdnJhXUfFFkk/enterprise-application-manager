FROM python:3.13.2-alpine3.21@sha256:323a717dc4a010fee21e3f1aac738ee10bb485de4e7593ce242b36ee48d6b352

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /shared-volume

COPY requirements.txt /shared-volume/
RUN pip install --no-cache-dir --requirement requirements.txt
COPY . /shared-volume/

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:50479"]