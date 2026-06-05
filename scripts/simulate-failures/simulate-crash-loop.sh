#!/bin/bash

echo "🔴 Simulating service crash..."
echo "Stopping order-service container"
echo "Watch Grafana at http://localhost:3001"
echo "-------------------------------------------"

# Stop the order-service container
docker-compose stop order-service

echo "✅ order-service is now DOWN!"
echo ""
echo "Check these things now:"
echo "1. Go to http://localhost:3000/health"
echo "   → Should show connection refused"
echo ""
echo "2. Go to Prometheus http://localhost:9090"
echo "   → Status > Targets"
echo "   → order-service should show DOWN (red)"
echo ""
echo "3. Check Grafana query:"
echo "   up{job='order-service'}"
echo "   → Should show 0 (down)"
echo ""
echo "To fix run: ./scripts/simulate-failures/cleanup-failures.sh"