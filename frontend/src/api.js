// Central API configuration
const getApiBaseUrl = () => {
    if (process.env.REACT_APP_API_URL) {
        return process.env.REACT_APP_API_URL.replace(/\/+$/, '');
    }
    if (typeof window !== 'undefined' && window.location.hostname && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
        return `http://${window.location.hostname}:8000`;
    }
    return 'http://localhost:8000';
};

export const API_BASE_URL = getApiBaseUrl();
export default API_BASE_URL;
