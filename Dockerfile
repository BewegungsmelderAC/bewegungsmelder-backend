FROM python:3
ENV LC_ALL 'C.UTF-8'
ENV LANG 'C.UTF-8'
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "app.py"]