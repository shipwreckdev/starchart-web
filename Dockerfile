FROM python:3.7-slim-stretch

# Install nmap.
RUN apt-get update -y && \
    apt-get install nmap -y && \
    apt-get clean

# Copy repo files into svc directory.
COPY . /service

# Set the work directory to the app folder.
WORKDIR /service

# Set up env for app.
RUN pip3 install pipenv && \
    pipenv install && \
    pipenv run python3 manage.py migrate && \
    pipenv run python3 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('starchart', 'admin@shipwreck.dev', 'starchart')"

CMD pipenv run python3 manage.py runserver 0.0.0.0:8000
