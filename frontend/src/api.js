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