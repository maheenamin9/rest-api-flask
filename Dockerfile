# how to create image
FROM python:3.11
WORKDIR /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
# commands that run when this image starts up as container
# CMD ["flask", "run", "--host", "0.0.0.0"]
# CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]
CMD ["/bin/bash", "docker-entrypoint.sh"]