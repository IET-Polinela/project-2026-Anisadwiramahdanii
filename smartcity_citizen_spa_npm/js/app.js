let currentDashboardTab = 'my_reports';
let currentDashboardPage = 1;
let editingReportId = null;
let reportModal = null;

async function setupDashboard() {
    const reloadButton = document.getElementById('reloadReports');
    const openReportModalButton = document.getElementById('btnBukaModal');
    const reportsPagination = document.getElementById('paginationContainer');

    if (reloadButton) {
        reloadButton.addEventListener('click', function () {
            loadDashboardData(currentDashboardTab, currentDashboardPage);
        });
    }

    if (openReportModalButton) {
        openReportModalButton.addEventListener('click', openCreateReportModal);
    }

    document.querySelectorAll('[data-dashboard-tab]').forEach(function (button) {
        button.addEventListener('click', function () {
            loadDashboardData(button.dataset.dashboardTab, 1);
        });
    });

    if (reportsPagination) {
        reportsPagination.addEventListener('click', function (event) {
            const button = event.target.closest('[data-page]');

            if (!button || button.disabled) {
                return;
            }

            loadDashboardData(currentDashboardTab, Number(button.dataset.page));
        });
    }

    setupReportForm();
    await loadDashboardData(currentDashboardTab, currentDashboardPage);
}

async function loadDashboardData(tab = currentDashboardTab, page = currentDashboardPage) {
    const target = document.getElementById('listContainer');

    currentDashboardTab = tab;
    currentDashboardPage = page;
    updateDashboardTabUI(tab);

    if (target) {
        target.innerHTML = '<div class="text-secondary text-center py-4">Memuat laporan...</div>';
    }

    try {
        const result = await requestAPI(`/api/report/?tab=${tab}&page=${page}`, 'GET');
        const payload = result.data || { results: [], count: 0 };
        const reports = payload.results || [];

        renderList(reports, tab);
        renderPagination(payload, page);
        await loadSummaryStats();
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

async function loadSummaryStats() {
    try {
        const result = await requestAPI('/api/report/?tab=my_reports&page_size=1000', 'GET');
        const reports = result.data.results || [];
        updateDashboardStats(reports);
    } catch (error) {
        updateDashboardStats([]);
    }
}

function updateDashboardTabUI(tab) {
    const title = document.getElementById('dashboardPanelTitle');

    document.querySelectorAll('[data-dashboard-tab]').forEach(function (button) {
        const isActive = button.dataset.dashboardTab === tab;
        button.classList.toggle('btn-primary', isActive);
        button.classList.toggle('btn-outline-primary', !isActive);
    });

    if (title) {
        title.textContent = tab === 'feed' ? 'Feed Kota' : 'Laporan Saya';
    }
}

function setupReportForm() {
    const modalElement = document.getElementById('reportModal');
    const saveDraftButton = document.getElementById('btnDraft');
    const submitReportButton = document.getElementById('btnSubmit');

    if (!modalElement || !window.bootstrap) {
        return;
    }

    reportModal = bootstrap.Modal.getOrCreateInstance(modalElement);

    modalElement.addEventListener('hidden.bs.modal', function () {
        resetReportForm();
    });

    if (saveDraftButton) {
        saveDraftButton.onclick = function () {
            submitReportForm('DRAFT');
        };
    }

    if (submitReportButton) {
        submitReportButton.onclick = function () {
            submitReportForm('REPORTED');
        };
    }
}

function openCreateReportModal() {
    resetReportForm();
    const title = document.getElementById('reportModalLabel');

    if (title) {
        title.textContent = 'Buat Laporan Baru';
    }

    if (reportModal) {
        reportModal.show();
    }
}

async function editDraft(id) {
    try {
        const result = await requestAPI(`/api/reports/${id}/`, 'GET');
        const report = result.data;

        if (report.status !== 'DRAFT') {
            return;
        }

        editingReportId = id;
        fillReportForm(report);

        const title = document.getElementById('reportModalLabel');
        if (title) {
            title.textContent = 'Edit Draft Laporan';
        }

        if (reportModal) {
            reportModal.show();
        }
    } catch (error) {
        showReportFormAlert('Draft tidak bisa dimuat untuk diedit.', 'danger');
    }
}

function fillReportForm(report) {
    const form = document.getElementById('reportForm');

    if (!form) {
        return;
    }

    form.elements.title.value = report.title || '';
    form.elements.category.value = report.category || '';
    form.elements.location.value = report.location || '';
    form.elements.description.value = report.description || '';
}

async function submitReportForm(status) {
    const form = document.getElementById('reportForm');

    if (!form || !form.reportValidity()) {
        return;
    }

    const payload = {
        title: form.elements.title.value.trim(),
        category: form.elements.category.value,
        location: form.elements.location.value.trim(),
        description: form.elements.description.value.trim(),
        status,
    };
    const isEditing = editingReportId !== null;
    const endpoint = isEditing ? `/api/report/${editingReportId}/` : '/api/report/';
    const method = isEditing ? 'PUT' : 'POST';

    try {
        const result = await requestAPI(endpoint, method, payload);

        if ([200, 201].includes(result.status)) {
            if (reportModal) {
                reportModal.hide();
            }

            resetReportForm();
            alert(`Laporan berhasil disimpan sebagai ${status}`);
            await loadDashboardData('my_reports', 1);
        }
    } catch (error) {
        showReportFormAlert('Laporan belum bisa disimpan. Periksa kembali data form.', 'danger');
    }
}

function resetReportForm() {
    const form = document.getElementById('reportForm');
    const alertBox = document.getElementById('reportFormAlert');

    if (form) {
        form.reset();
    }

    editingReportId = null;

    if (alertBox) {
        alertBox.className = 'alert d-none';
        alertBox.textContent = '';
    }
}

function showReportFormAlert(message, type) {
    const alertBox = document.getElementById('reportFormAlert');

    if (!alertBox) {
        return;
    }

    alertBox.className = `alert alert-${type}`;
    alertBox.textContent = message;
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
