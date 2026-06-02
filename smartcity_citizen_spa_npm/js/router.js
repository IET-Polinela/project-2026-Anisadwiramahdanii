const routes = {
    login: {
        render: loginView,
        afterRender: setupLoginForm,
        public: true,
    },
    dashboard: {
        render: dashboardView,
        afterRender: function () {
            setupDashboard();
        },
        public: false,
    },
};

function getCurrentRoute() {
    return window.location.hash.replace('#', '') || 'dashboard';
}

function router() {
    const routeName = getCurrentRoute();
    const route = routes[routeName] || routes.dashboard;
    const app = document.getElementById('app');

    if (!route.public && !isAuthenticated()) {
        window.location.hash = '#login';
        return;
    }

    app.innerHTML = route.render();
    route.afterRender();
    updateActiveNav(routeName);
    updateAuthUI();
}

function updateActiveNav(routeName) {
    document.querySelectorAll('[data-route-link]').forEach(function (link) {
        link.classList.toggle('active', link.dataset.routeLink === routeName);
    });
}
