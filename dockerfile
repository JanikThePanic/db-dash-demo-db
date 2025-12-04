# ---- Base image ----
FROM python:3.12-slim

# ---- Set working dir ----
WORKDIR /app

# ---- Install dependencies ----
# Using no-cache for small image size
RUN pip install --no-cache-dir \
    weaviate-client \
    kagglehub \
    pandas \
    scikit-learn

# ---- Copy script ----
COPY load_data.py .

# ---- Run script ----
CMD ["python", "load_data.py"]