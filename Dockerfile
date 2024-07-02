# Use the official Python image as a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install langchain
RUN pip install langchain==0.0.333
RUN pip install beautifulsoup4==4.12.3

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the Flask app code to the working directory
COPY app.py .

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run your Flask app
CMD ["python", "app.py"]