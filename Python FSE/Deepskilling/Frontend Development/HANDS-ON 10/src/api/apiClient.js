import axios from 'axios';

// Task 1, step 138: single configured Axios instance
const apiClient = axios.create({
  baseURL: 'https://jsonplaceholder.typicode.com',
  timeout: 5000,
  headers: { 'Content-Type': 'application/json' }
});

// Task 1, step 141: request interceptor attaches a mock auth token
apiClient.interceptors.request.use((config) => {
  config.headers.Authorization = 'Bearer mock-token-123';
  return config;
});

// Task 1, step 140: response interceptor unwraps data and standardises errors
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const statusCode = error.response ? error.response.status : 0;
    const message = error.response
      ? `Request failed with status ${statusCode}`
      : 'Network error - please check your connection';
    return Promise.reject({ message, statusCode });
  }
);

export default apiClient;
