# Use the official Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container at /app
COPY get-likes.py /app/

# Run the Python script when the container launches
CMD ["python", "./get-likes.py"]
