FROM python:3

ENV FLASK_APP 'app'
ENV LC_ALL 'C.UTF-8'
ENV LANG 'C.UTF-8'
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "30", "app:create_app()"]