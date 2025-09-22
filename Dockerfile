FROM python:3.13.7
WORKDIR /usr/src/main
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "./main.py"]