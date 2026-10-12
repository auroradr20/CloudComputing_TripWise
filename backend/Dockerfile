FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend

ENV FLASK_APP=backend.app:create_app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001

EXPOSE 5001

CMD ["flask", "run"]