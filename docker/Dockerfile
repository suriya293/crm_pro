FROM python:3.10-slim-bullseye as base

# Install system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    curl \
    git \
    libpq-dev \
    postgresql-client \
    redis-tools \
    && rm -rf /var/lib/apt/lists/*

# Add frappe user
RUN useradd -ms /bin/bash frappe
USER frappe
WORKDIR /home/frappe

# Install bench
RUN pip install --user frappe-bench

# Set path
ENV PATH="/home/frappe/.local/bin:${PATH}"

# Initialize bench
RUN bench init --skip-redis-config-files --skip-assets --frappe-branch version-15 frappe-bench

WORKDIR /home/frappe/frappe-bench

# Add custom app
COPY --chown=frappe:frappe . apps/crm_pro
RUN bench get-app --local apps/crm_pro

EXPOSE 8000 9000
