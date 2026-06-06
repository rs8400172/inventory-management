import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      console.error('Unauthorized');
    }
    return Promise.reject(error);
  }
);

// ==================== PRODUCTS ====================

export const productService = {
  getAll: (skip = 0, limit = 10) =>
    api.get('/products', { params: { skip, limit } }),
  
  getById: (id) =>
    api.get(`/products/${id}`),
  
  create: (data) =>
    api.post('/products', data),
  
  update: (id, data) =>
    api.put(`/products/${id}`, data),
  
  delete: (id) =>
    api.delete(`/products/${id}`),
};

// ==================== CUSTOMERS ====================

export const customerService = {
  getAll: (skip = 0, limit = 10) =>
    api.get('/customers', { params: { skip, limit } }),
  
  getById: (id) =>
    api.get(`/customers/${id}`),
  
  create: (data) =>
    api.post('/customers', data),
  
  update: (id, data) =>
    api.put(`/customers/${id}`, data),
  
  delete: (id) =>
    api.delete(`/customers/${id}`),
};

// ==================== ORDERS ====================

export const orderService = {
  getAll: (skip = 0, limit = 10) =>
    api.get('/orders', { params: { skip, limit } }),
  
  getById: (id) =>
    api.get(`/orders/${id}`),
  
  create: (data) =>
    api.post('/orders', data),
  
  delete: (id) =>
    api.delete(`/orders/${id}`),
};

// ==================== DASHBOARD ====================

export const dashboardService = {
  getStats: () =>
    api.get('/dashboard'),
};

export default api;
