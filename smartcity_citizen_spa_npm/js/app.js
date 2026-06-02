async function setupDashboard() {
    const reloadButton = document.getElementById('reloadReports');

    if (reloadButton) {
        reloadButton.addEventListener('click', loadDashboardReports);
    }

    await loadDashboardReports();
}

async function loadDashboardReports() {
    const target = document.getElementById('reportsList');

    if (target) {
        target.innerHTML = '<div class="text-secondary text-center py-4">Memuat laporan...</div>';
    }

    try {
        const result = await requestAPI('/api/reports/', 'GET');
        const reports = Array.isArray(result.data) ? result.data : result.data.results || [];

        renderReportCards(reports);
        updateDashboardStats(reports);
    } catch (error) {
        if (error.response && error.response.status === 401) {
            logout();
            return;
        }

        if (target) {
            target.innerHTML = '<div class="alert alert-warning mb-0">Data laporan belum bisa dimuat. Pastikan backend Django berjalan di port 8000.</div>';
        }
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const logoutButton = document.getElementById('logoutButton');

    if (logoutButton) {
        logoutButton.addEventListener('click', logout);
    }

    if (!window.location.hash) {
        window.location.hash = isAuthenticated() ? '#dashboard' : '#login';
    }

    updateAuthUI();
    router();
});

window.addEventListener('hashchange', router);
