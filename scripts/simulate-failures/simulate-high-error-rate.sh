#!/bin/bash

echo "🔴 Simulating high error rate on order-service..."
echo "Sending 50 bad requests with missing fields"
echo "Watch Grafana at http://localhost:3001"
echo "-------------------------------------------"

for i in {1..50}; do
  # Send request with missing required fields → returns 400
  curl -s -X POST http://localhost:3000/orders \
    -H "Content-Type: application/json" \
    -d '{"wrong_field": "bad data"}' > /dev/null
  
  # Send request to non-existent endpoint → returns 404  
  curl -s http://localhost:3000/nonexistent > /dev/null
  
  echo "Bad request batch $i/50 sent"
  sleep 0.5
done

echo "-------------------------------------------"
echo "✅ Simulation complete!"
echo "Check Grafana query:"
echo "rate(http_requests_total{status_code=~'4..'}[5m]) / rate(http_requests_total[5m]) * 100"