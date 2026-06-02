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
                <a class="btn btn-primary" href="#login">
                    <i class="bi bi-shield-lock me-1"></i>Kelola Sesi
                </a>
            </div>

            <div class="row g-3">
                <aside class="col-12 col-lg-3">
                    <div class="panel h-100">
                        <div class="panel-header">
                            <h2 class="h6 mb-0">Ringkasan</h2>
                        </div>
                        <div class="panel-body d-grid gap-3">
                            <div class="metric">
                                <div class="text-secondary small">Total Laporan</div>
                                <div class="metric-value" id="totalReports">0</div>
                            </div>
                            <div class="metric">
                                <div class="text-secondary small">Draft</div>
                                <div class="metric-value" id="draftReports">0</div>
                            </div>
                            <div class="metric">
                                <div class="text-secondary small">Diproses</div>
                                <div class="metric-value" id="activeReports">0</div>
                            </div>
                        </div>
                    </div>
                </aside>

                <section class="col-12 col-lg-6">
                    <div class="panel">
                        <div class="panel-header d-flex justify-content-between align-items-center gap-2">
                            <div>
                                <h2 class="h6 mb-0">Laporan Terbaru</h2>
                                <span class="text-secondary small">Prioritas pemantauan warga.</span>
                            </div>
                            <button class="btn btn-outline-primary btn-sm" id="reloadReports" type="button" title="Muat ulang">
                                <i class="bi bi-arrow-clockwise"></i>
                            </button>
                        </div>
                        <div class="panel-body">
                            <div id="reportsList" class="d-grid gap-3">
                                <div class="text-secondary text-center py-4">Memuat laporan...</div>
                            </div>
                        </div>
                    </div>
                </section>

                <aside class="col-12 col-lg-3">
                    <div class="panel h-100">
                        <div class="panel-header">
                            <h2 class="h6 mb-0">Aktivitas</h2>
                        </div>
                        <div class="panel-body d-grid gap-3">
                            <div class="activity-item">
                                <span class="activity-icon"><i class="bi bi-key"></i></span>
                                <div>
                                    <div class="fw-semibold">Sesi aktif</div>
                                    <div class="text-secondary small">Akses warga tersambung ke layanan kota.</div>
                                </div>
                            </div>
                            <div class="activity-item">
                                <span class="activity-icon"><i class="bi bi-diagram-3"></i></span>
                                <div>
                                    <div class="fw-semibold">Navigasi cepat</div>
                                    <div class="text-secondary small">Dashboard siap dipakai untuk pemantauan harian.</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </aside>
            </div>
        </section>
    `;
}

function renderReportCards(reports) {
    const target = document.getElementById('reportsList');

    if (!target) {
        return;
    }

    if (!reports.length) {
        target.innerHTML = '<div class="text-secondary text-center py-4">Belum ada laporan yang dapat ditampilkan.</div>';
        return;
    }

    target.innerHTML = reports.slice(0, 5).map(function (report) {
        return `
            <article class="report-card p-3">
                <div class="d-flex justify-content-between gap-3 mb-2">
                    <h3 class="h6 mb-0">${escapeHTML(report.title)}</h3>
                    <span class="badge text-bg-primary">${escapeHTML(report.status)}</span>
                </div>
                <p class="text-secondary small mb-2">${escapeHTML(report.description || '').slice(0, 140)}</p>
                <div class="d-flex flex-wrap gap-3 text-secondary small">
                    <span><i class="bi bi-pin-map me-1"></i>${escapeHTML(report.location || '-')}</span>
                    <span><i class="bi bi-tag me-1"></i>${escapeHTML(report.category || '-')}</span>
                </div>
            </article>
        `;
    }).join('');
}

function updateDashboardStats(reports) {
    const totalReports = document.getElementById('totalReports');
    const draftReports = document.getElementById('draftReports');
    const activeReports = document.getElementById('activeReports');

    if (!totalReports || !draftReports || !activeReports) {
        return;
    }

    totalReports.textContent = reports.length;
    draftReports.textContent = reports.filter((report) => report.status === 'DRAFT').length;
    activeReports.textContent = reports.filter((report) => ['REPORTED', 'VERIFIED', 'IN_PROGRESS'].includes(report.status)).length;
}

function escapeHTML(value) {
    return String(value)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#039;');
}
