const request = require('supertest');
const app = require('../server');

describe('Order Service API', () => {
  
  describe('GET /health', () => {
    it('should return healthy status', async () => {
      const res = await request(app).get('/health');
      expect(res.statusCode).toBe(200);
      expect(res.body.status).toBe('healthy');
      expect(res.body.service).toBe('order-service');
    });
  });

  describe('GET /orders', () => {
    it('should return list of orders', async () => {
      const res = await request(app).get('/orders');
      expect(res.statusCode).toBe(200);
      expect(res.body.orders).toBeDefined();
      expect(res.body.total).toBeGreaterThan(0);
    });
  });

  describe('POST /orders', () => {
    it('should create a new order', async () => {
      const res = await request(app)
        .post('/orders')
        .send({ item: 'Zinger Burger', restaurant: 'KFC' });
      expect(res.statusCode).toBe(201);
      expect(res.body.item).toBe('Zinger Burger');
      expect(res.body.status).toBe('pending');
    });

    it('should return 400 if item is missing', async () => {
      const res = await request(app)
        .post('/orders')
        .send({ restaurant: 'KFC' });
      expect(res.statusCode).toBe(400);
      expect(res.body.error).toBeDefined();
    });

    it('should return 400 if restaurant is missing', async () => {
      const res = await request(app)
        .post('/orders')
        .send({ item: 'Zinger Burger' });
      expect(res.statusCode).toBe(400);
      expect(res.body.error).toBeDefined();
    });
  });

});