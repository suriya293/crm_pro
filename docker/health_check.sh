#!/bin/bash
# LeadsCRM Production Health Check Script

set -eo pipefail

echo "=== Checking LeadsCRM Services Health ==="

# 1. Check if backend port 8000 is open and responding
echo "Checking web server connection..."
if curl -s -f http://localhost:8000/api/method/frappe.ping > /dev/null; then
    echo "Web Server (Frappe): HEALTHY"
else
    echo "Web Server (Frappe): UNHEALTHY"
    exit 1
fi

# 2. Check scheduler status via bench execute
echo "Checking background task scheduler..."
if bench doctor | grep -q "Workers online"; then
    echo "Scheduler & workers: HEALTHY"
else
    echo "Scheduler & workers: UNHEALTHY"
    exit 1
fi

# 3. Check Redis ping
echo "Checking Redis Cache..."
if redis-cli -h redis-cache ping | grep -q "PONG"; then
    echo "Redis Cache: HEALTHY"
else
    echo "Redis Cache: UNHEALTHY"
    exit 1
fi

echo "=== All services are HEALTHY ==="
exit 0
