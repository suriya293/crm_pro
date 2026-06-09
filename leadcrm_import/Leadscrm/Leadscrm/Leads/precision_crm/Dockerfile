FROM frappe/frappe-worker:v16.0.0

# Install custom app dependencies
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

USER frappe

# Install precision_crm app
RUN bench get-app --branch main precision_crm https://github.com/user/precision_crm.git
