FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app folder into the container
COPY app app

# Add current directory to PYTHONPATH so "app" becomes importable
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Default run command
CMD ["python", "app/main.py"]
