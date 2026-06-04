const express = require('express');
const client = require('prom-client');

const app = express();
app.use(express.json());

// Prometheus metrics setup
const register = new client.Registry();
client.collectDefaultMetrics({ register });

const httpRequestCounter = new client.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code'],
  registers: [register]
});

const httpRequestDuration = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route'],
  registers: [register]
});

// In-memory orders store
let orders = [
  { id: 1, item: 'Zinger Burger', status: 'delivered', restaurant: 'KFC' },
  { id: 2, item: 'Pepperoni Pizza', status: 'preparing', restaurant: 'Pizza Hut' },
  { id: 3, item: 'Crunchwrap', status: 'pending', restaurant: 'Taco Bell' }
];

// Middleware to track metrics for every request
app.use((req, res, next) => {
  const end = httpRequestDuration.startTimer({ 
    method: req.method, 
    route: req.path 
  });
  res.on('finish', () => {
    httpRequestCounter.inc({ 
      method: req.method, 
      route: req.path, 
      status_code: res.statusCode 
    });
    end();
  });
  next();
});

// Routes
app.get('/health', (req, res) => {
  res.status(200).json({ 
    status: 'healthy', 
    service: 'order-service',
    timestamp: new Date().toISOString()
  });
});

app.get('/orders', (req, res) => {
  res.status(200).json({ 
    orders,
    total: orders.length 
  });
});

app.post('/orders', (req, res) => {
  const { item, restaurant } = req.body;
  if (!item || !restaurant) {
    return res.status(400).json({ 
      error: 'item and restaurant are required' 
    });
  }
  const newOrder = {
    id: orders.length + 1,
    item,
    restaurant,
    status: 'pending'
  };
  orders.push(newOrder);
  res.status(201).json(newOrder);
});

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Order service running on port ${PORT}`);
});

module.exports = app;