FROM python:3.12.8

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install -upgrade pip
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
RUN mkdir /app/static

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "habithub.wsgi:application"]
