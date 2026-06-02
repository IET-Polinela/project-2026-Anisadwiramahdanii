const API_BASE_URL = 'http://127.0.0.1:8000';

async function requestAPI(endpoint, method = 'GET', bodyData = null) {
    const headers = {
        Accept: 'application/json',
        'Content-Type': 'application/json',
    };
    const accessToken = localStorage.getItem('access_token');

    if (accessToken) {
        headers.Authorization = `Bearer ${accessToken}`;
    }

    const options = {
        method,
        headers,
    };

    if (bodyData) {
        options.body = JSON.stringify(bodyData);
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
    const contentType = response.headers.get('content-type') || '';
    const data = contentType.includes('application/json') ? await response.json() : null;

    if (!response.ok) {
        const error = new Error('Request gagal');
        error.response = response;
        error.data = data;
        throw error;
    }

    return {
        status: response.status,
        data,
    };
}
