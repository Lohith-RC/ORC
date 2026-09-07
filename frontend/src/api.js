import axios from 'axios';

// Central API configuration
const getApiBaseUrl = () => {
    if (process.env.REACT_APP_API_URL) {
        return process.env.REACT_APP_API_URL.replace(/\/+$/, '');
    }
    // ponytail: fallback to live Cloudflare tunnel on HTTPS, localhost on local dev
    if (typeof window !== 'undefined' && window.location.protocol === 'https:') {
        return 'https://gathered-download-cognitive-comparing.trycloudflare.com';
    }
    return 'http://localhost:8000';
};

export const API_BASE_URL = getApiBaseUrl();

// Global 401 Auth Interceptor: clear stale tokens and redirect to login
axios.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            localStorage.removeItem('token');
            if (typeof window !== 'undefined' && !window.location.pathname.includes('/login')) {
                window.location.href = '/login?expired=1';
            }
        }
        return Promise.reject(error);
    }
);

// Authenticated fetch wrapper for REST APIs
export const authFetch = async (endpoint, options = {}) => {
    const token = localStorage.getItem('token');
    const url = endpoint.startsWith('http') ? endpoint : `${API_BASE_URL}${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;
    const headers = {
        ...(options.headers || {}),
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    };
    const res = await fetch(url, { ...options, headers });
    if (res.status === 401) {
        localStorage.removeItem('token');
        if (typeof window !== 'undefined' && !window.location.pathname.includes('/login')) {
            window.location.href = '/login?expired=1';
        }
    }
    return res;
};

export default API_BASE_URL;
