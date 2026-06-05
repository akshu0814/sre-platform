#!/bin/bash

echo "🟢 Cleaning up all simulated failures..."
echo "-------------------------------------------"

# Restart order-service if stopped
echo "Starting order-service..."
docker-compose start order-service

# Wait for it to be healthy
echo "Waiting for order-service to be healthy..."
sleep 5

# Verify it's back up
HEALTH=$(curl -s http://localhost:3000/health | grep -c "healthy")

if [ $HEALTH -eq 1 ]; then
  echo "✅ order-service is back UP and healthy!"
else
  echo "❌ order-service is still down, checking logs..."
  docker-compose logs order-service --tail=20
fi

echo ""
echo "-------------------------------------------"
echo "🟢 All services restored!"
echo "Verify in Grafana: up{job='order-service'} should show 1"