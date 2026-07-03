function loginView() {
    return `
        <section class="login-wrap">
            <div class="panel">
                <div class="panel-header">
                    <h1 class="h4 mb-1">Login Warga</h1>
                    <p class="text-secondary mb-0">Masuk menggunakan akun yang terdaftar di backend Django.</p>
                </div>
                <div class="panel-body">
                    <div id="loginAlert" class="alert d-none" role="alert"></div>
                    <form id="loginForm" autocomplete="on">
                        <div class="mb-3">
                            <label for="username" class="form-label">Username</label>
                            <div class="input-group">
                                <span class="input-group-text"><i class="bi bi-person"></i></span>
                                <input class="form-control" id="username" name="username" required>
                            </div>
                        </div>
                        <div class="mb-4">
                            <label for="password" class="form-label">Password</label>
                            <div class="input-group">
                                <span class="input-group-text"><i class="bi bi-lock"></i></span>
                                <input class="form-control" id="password" name="password" type="password" required>
                            </div>
                        </div>
                        <button class="btn btn-primary w-100" type="submit">
                            <i class="bi bi-box-arrow-in-right me-1"></i>Login
                        </button>
                    </form>
                </div>
            </div>
        </section>
    `;
}

function dashboardView() {
    return `
        <section class="workspace">
            <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-3">
                <div>
                    <h1 class="h3 mb-1">Dashboard Citizen</h1>
                    <p class="text-secondary mb-0">Pantau laporan kota dan status pengaduan warga.</p>
                </div>
               <button class="btn btn-primary" id="btnBukaModal" type="button">
                   <i class="bi bi-plus-lg me-1"></i>Tambah Laporan Baru
               </button>
            </div>

            <div class="row g-3">
                <aside class="col-12 col-lg-3">
                    <div class="panel h-100">
                        <div class="panel-header">
                            <h2 class="h6 mb-0">Ringkasan</h2>
                        </div>
                        <div class="panel-body d-grid gap-3" id="summaryStats">
                            <div class="metric">
                                <div class="text-secondary small">Total Laporan</div>
                                <div class="metric-value" id="totalReports">0</div>
                            </div>
                            <div class="metric">
                                <div class="text-secondary small">Draft</div>
                                <div class="metric-value badge bg-secondary" id="draftReports">0</div>
                            </div>
                            <div class="metric">
                                <div class="text-secondary small">Diproses</div>
                                <div class="metric-value" id="activeReports">0</div>
                            </div>
                            <div class="metric">
                                <div class="text-secondary small">Selesai</div>
                                <div class="metric-value" id="resolvedReports">0</div>
                            </div>
                        </div>
                    </div>
                </aside>

                <section class="col-12 col-lg-9">
                    <div class="panel">
                        <div class="panel-header d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3">
                            <div>
                                <h2 class="h6 mb-0" id="dashboardPanelTitle">Laporan Saya</h2>
                                <span class="text-secondary small">Data dimuat dari API secara terpaginasi.</span>
                            </div>
                            <div class="d-flex gap-2">
                                <div class="btn-group btn-group-sm" role="tablist" aria-label="Filter laporan">
                                    <button class="btn btn-primary" id="myReportsTab" type="button" data-dashboard-tab="my_reports">
                                        <i class="bi bi-person-lines-fill me-1"></i>Laporan Saya
                                    </button>
                                   <button class="btn btn-outline-primary"
                                           id="tabFeedKota"
                                           type="button"
                                           data-dashboard-tab="feed">
                                       <i class="bi bi-broadcast me-1"></i>Feed Kota
                                    </button>
                                </div>
                                <button class="btn btn-outline-primary btn-sm" id="reloadReports" type="button" title="Muat ulang">
                                    <i class="bi bi-arrow-clockwise"></i>
                                </button>
                            </div>
                        </div>
                        <div class="panel-body">
                            <div id="listContainer" class="row g-3">
                                <div class="text-secondary text-center py-4">Memuat laporan...</div>
                            </div>
                            <nav class="mt-3" aria-label="Navigasi halaman laporan">
                                <div id="paginationContainer" class="pagination pagination-sm mb-0 justify-content-center"></div>
                            </nav>
                        </div>
                    </div>
                </section>
            </div>
        </section>
    `;
}

function renderList(reports, tab) {
    const target = document.getElementById('listContainer');

    if (!target) {
        return;
    }

    if (!reports.length) {
        target.innerHTML = '<div class="text-secondary text-center py-4">Belum ada laporan yang dapat ditampilkan.</div>';
        return;
    }

    target.innerHTML = reports.map(function (report) {
        const statusInfo = getStatusInfo(report.status);
        const canEditDraft = tab === 'my_reports' && report.is_owner && report.status === 'DRAFT';
        const updatedAt = report.updated_at ? new Date(report.updated_at).toLocaleString('id-ID') : '-';

        return `
        <div class="col">
            <article class="report-card">
                <div class="d-flex flex-column flex-md-row justify-content-between gap-2 mb-2">
                    <div>
                        <h3 class="h6 mb-1">${escapeHTML(report.title)}</h3>
                        <div class="d-flex flex-wrap gap-3 text-secondary small">
                            <span><i class="bi bi-person me-1"></i>${escapeHTML(report.reporter || 'Warga Anonim')}</span>
                            <span><i class="bi bi-clock-history me-1"></i>${escapeHTML(updatedAt)}</span>
                        </div>
                    </div>
                    <span class="badge ${statusInfo.badgeClass} align-self-start">${statusInfo.label}</span>
                </div>
                <p class="text-secondary small mb-2">${escapeHTML(report.description || '').slice(0, 140)}</p>
                <div class="d-flex flex-wrap gap-3 text-secondary small">
                    <span><i class="bi bi-pin-map me-1"></i>${escapeHTML(report.location || '-')}</span>
                    <span><i class="bi bi-tag me-1"></i>${escapeHTML(report.category || '-')}</span>
                </div>
                <div class="progress report-progress mt-3" role="progressbar" aria-label="Progress ${statusInfo.label}" aria-valuenow="${statusInfo.progress}" aria-valuemin="0" aria-valuemax="100">
                    <div class="progress-bar ${statusInfo.progressClass}" style="width: ${statusInfo.progress}%">${statusInfo.progress}%</div>
                </div>
                ${canEditDraft ? `
                    <div class="d-flex justify-content-end mt-3">
                        <button class="btn btn-outline-primary btn-sm" type="button" onclick="editDraft(${report.id})">
                            <i class="bi bi-pencil-square me-1"></i>Edit Draft
                        </button>
                    </div>
                ` : ''}
            </article>
        </div>
        `;
    }).join('');
}

function renderPagination(payload, currentPage) {
    const target = document.getElementById('paginationContainer');

    if (!target) {
        return;
    }

    const totalPages = Math.max(1, Math.ceil((payload.count || 0) / 10));

    if (totalPages <= 1) {
        target.innerHTML = '';
        return;
    }

    const items = [];
    items.push(paginationButton('Prev', currentPage - 1, currentPage === 1));

    for (let page = 1; page <= totalPages; page += 1) {
        items.push(paginationButton(String(page), page, false, page === currentPage));
    }

    items.push(paginationButton('Next', currentPage + 1, currentPage === totalPages));
    target.innerHTML = items.join('');
}

function paginationButton(label, page, disabled, active) {
    return `
        <button class="page-item btn page-link ${active ? 'active' : ''}" type="button" ${disabled ? 'disabled' : ''} data-page="${page}">
            ${escapeHTML(label)}
        </button>
    `;
}

function updateDashboardStats(reports) {
    const totalReports = document.getElementById('totalReports');
    const draftReports = document.getElementById('draftReports');
    const activeReports = document.getElementById('activeReports');
    const resolvedReports = document.getElementById('resolvedReports');

    if (!totalReports || !draftReports || !activeReports || !resolvedReports) {
        return;
    }

    totalReports.textContent = reports.length;
    draftReports.textContent = reports.filter((report) => report.status === 'DRAFT').length;
    activeReports.textContent = reports.filter((report) => ['REPORTED', 'VERIFIED', 'IN_PROGRESS'].includes(report.status)).length;
    resolvedReports.textContent = reports.filter((report) => report.status === 'RESOLVED').length;
}

function getStatusInfo(status) {
    const statuses = {
        DRAFT: { label: 'Draft', progress: 10, badgeClass: 'text-bg-secondary', progressClass: 'bg-secondary' },
        REPORTED: { label: 'Dilaporkan', progress: 35, badgeClass: 'text-bg-warning', progressClass: 'bg-warning' },
        VERIFIED: { label: 'Diverifikasi', progress: 55, badgeClass: 'text-bg-info', progressClass: 'bg-info' },
        IN_PROGRESS: { label: 'Diproses', progress: 80, badgeClass: 'text-bg-primary', progressClass: 'bg-primary' },
        RESOLVED: { label: 'Selesai', progress: 100, badgeClass: 'text-bg-success', progressClass: 'bg-success' },
    };

    return statuses[status] || { label: status || '-', progress: 0, badgeClass: 'text-bg-light', progressClass: '' };
}

function escapeHTML(value) {
    return String(value)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#039;');
}
