FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install build tools needed for SHAP and others
RUN apt-get update && \
    apt-get install -y gcc g++ build-essential && \
    apt-get clean

# Copy files and install Python packages
COPY . .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Optional: Default entrypoint for CLI usage (can be changed)
CMD ["python", "predict.py"]
