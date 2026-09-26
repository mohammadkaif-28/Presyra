FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Build tools required by native Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY requirements.txt .
COPY docker_packages ./docker_packages

# Install Presyra application dependencies
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# Install CPU-only PyTorch
RUN pip install --default-timeout=1000 --no-cache-dir \
    torch==2.14.0+cpu \
    --index-url https://download.pytorch.org/whl/cpu

# Install Resemblyzer without pulling another PyTorch version
RUN pip install --default-timeout=1000 --no-cache-dir \
    resemblyzer==0.1.4 --no-deps

# Copy Presyra source code
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]