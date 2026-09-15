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

# Expose port and start Streamlit app
EXPOSE 10000
CMD ["streamlit", "run", "app.py", "--server.port=10000", "--server.address=0.0.0.0"]