import { data } from 'autoprefixer';
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getAppliances = () => apiClient.get('/appliances/');
export const createAppliance = (data) => apiClient.post('/appliances/', data);
export const deleteAppliance = (id) => apiClient.delete(`/appliances/${id}`);

export const createTest = (data) => apiClient.post('/tests/', data);
export const getTests = () => apiClient.get('/tests/');
export const getTest = (id) => apiClient.get(`/tests/${id}`);

export const startFortiTest = (data) =>
  apiClient.post(`/fortimanager/forti_test`, data);

export const getFortiManagerStats = () =>
  apiClient.get('/stats/fortimanager/stats');
