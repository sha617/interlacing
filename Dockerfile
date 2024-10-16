# Use an official Python base image
FROM python:3.9-slim

# Install ImageMagick, fonts, and dependencies
RUN apt-get update && apt-get install -y \
    imagemagick \
    ghostscript \
    fonts-dejavu-core \
    && apt-get clean

# Install Wand Python library
RUN pip install --no-cache-dir wand

# Set the working directory in the container
WORKDIR /app

# Copy the interlacing script into the container
COPY interlace.py /app/interlace.py

# Set the script as the entrypoint
ENTRYPOINT ["python", "/app/interlace.py"]
