FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set environment variables
ENV PORT=10000
ENV PYTHONPATH=.

# Expose port and start Functions Framework
EXPOSE 10000
CMD ["python3", "-m", "functions_framework", "--target=audit_pipeline", "--source=main.py", "--port=10000"]
