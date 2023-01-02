# how to create image
FROM python:3.11
EXPOSE 5000
WORKDIR /app
RUN pip install -r requirements.txt
COPY . .
# commands that run when this image starts up as container
CMD ["flask", "run", "--host", "0.0.0.0"]