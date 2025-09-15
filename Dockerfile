# Use official Python image
FROM python:3.11-slim
EXPOSE 8000

# Set environment vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /myapp/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/  

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
