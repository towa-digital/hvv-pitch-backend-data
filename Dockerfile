FROM python:3.12-slim

WORKDIR /code

# Install sqlite3
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY ./requirements.txt /code/requirements.txt

# Copy the SQLite database file
COPY ./my_database.db /code/my_database.db

# Install requirements
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code

# Set the environment variable to tell the app where to find the database
ENV DATABASE_URL=sqlite:////code/my_database.db

CMD ["fastapi", "run", "main.py", "--port", "7555", "--workers", "4"]