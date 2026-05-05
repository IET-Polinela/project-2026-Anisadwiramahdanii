# Lab Dashboard Implementation Plan

## Status: In Progress

### 1. [x] Environment Analysis ✅
- main_app.models.Report: OK (fields match: reporter_name, title, category, description, location, status, created_at)
- dashboard_24782037.views.py: Partial (DashboardView + DashboardDataView JsonResponse ready)
- generate_data.py: Already exists and ready
- settings.py: dashboard app registered

### 2. [ ] Data Seeding
- [ ] Install faker: `pip install faker`
- [ ] Run: `python manage.py generate_data 1000`

### 3. [ ] Dashboard Backend Completion
- [ ] main_app/urls.py: Add report_detail_json for modal
- [ ] dashboard_24782037/urls.py: Wire DashboardView + DashboardDataView
- [ ] iet_24782037_2026/urls.py: Add dashboard URL

### 4. [ ] Frontend Templates & JS
- [ ] templates/dashboard_24782037/dashboard.html: Charts (Chart.js), live search, modal, tables
- [ ] CDN: Bootstrap 5, Chart.js

### 5. [ ] Testing & Commands
- [ ] python manage.py makemigrations
- [ ] python manage.py migrate  
- [ ] python manage.py runserver
- [ ] Test charts, search, modal via fetch

### 6. [ ] Final Deliverables
- [ ] Screenshot views.py
- [ ] Dashboard UI with charts
- [ ] Live search + modal demo
- [ ] Console JSON fetch

**Next Step:** Install faker & generate data
