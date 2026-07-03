function isAuthenticated() {
    return Boolean(localStorage.getItem('access_token'));
}

function setupLoginForm() {
    const loginForm = document.getElementById('loginForm');
    const alertBox = document.getElementById('loginAlert');

    if (!loginForm) {
        return;
    }

    loginForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        alertBox.className = 'alert d-none';
        alertBox.textContent = '';

        const payload = {
            username: loginForm.username.value.trim(),
            password: loginForm.password.value,
        };

        try {
            const result = await requestAPI('/api/token/', 'POST', payload);

            localStorage.setItem('access_token', result.data.access);
            localStorage.setItem('refresh_token', result.data.refresh);
            localStorage.setItem('username', payload.username);

            alert('Login berhasil.');
            window.location.hash = '#dashboard';
            updateAuthUI();
        } catch (error) {
            alertBox.className = 'alert alert-danger';
            alertBox.textContent = 'Login gagal. Periksa kembali username dan password.';
        }
    });
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('username');

    updateAuthUI();
    window.location.hash = '#login';
}

function updateAuthUI() {
    const logoutButton = document.getElementById('logoutButton');
    const loginLink = document.querySelector('[data-route-link="login"]');

    if (!logoutButton || !loginLink) {
        return;
    }

    logoutButton.classList.toggle('d-none', !isAuthenticated());
    loginLink.classList.toggle('d-none', isAuthenticated());
}
