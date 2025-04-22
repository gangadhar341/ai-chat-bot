import axios from "axios";

// Create an Axios instance
const api = axios.create({
  baseURL: process.env.REACT_APP_ARTHA_BACKEND_BASE_URL + "/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor to allow requests only from the root route
api.interceptors.request.use(
  (config) => {
    // Check if the current route is "/"
    if (window.location.pathname !== "/" || config.url !== "/") {
      throw new Error('Requests are only allowed from the root route ("/").');
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle responses globally
api.interceptors.response.use(
  (response) => {
    // Handle successful responses
    return response;
  },
  (error) => {
    // Handle errors globally
    if (error.response) {
      // Server responded with a status code outside the 2xx range
      console.error(
        "API Error:",
        error.response.data.message || error.response.statusText
      );
    } else if (error.request) {
      // Request was made but no response was received
      console.error("No response received from the server.");
    } else {
      // Something else happened while setting up the request
      console.error("Error:", error.message);
    }
    return Promise.reject(error);
  }
);

// Chat check API
export const sendQuery = (data = {}) => api.post("/", data);

export default api;
