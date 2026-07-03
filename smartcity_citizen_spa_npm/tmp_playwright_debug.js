const { chromium } = require('@playwright/test');
(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  const BASE_URL = 'http://103.151.63.85:8005';
  try {
    await page.goto(`${BASE_URL}/accounts/login/`, { waitUntil: 'networkidle' });
    console.log('login page url', page.url());
    console.log('title', await page.title());
    console.log('has username', await page.locator('input[name="username"]').count());
    console.log('has password', await page.locator('input[name="password"]').count());
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'admin123');
    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle', timeout: 20000 }).catch(e => { console.log('nav wait error', e.message); }),
      page.click('button[type="submit"]')
    ]);
    console.log('after submit url', page.url());
    console.log('body contains login', await page.locator('form').count());
    console.log('body text snippet', await page.textContent('body').then(t => t.slice(0, 600)));
    await page.goto(`${BASE_URL}/dashboard/`, { waitUntil: 'networkidle' });
    console.log('/dashboard url', page.url());
    console.log('reportedTable count', await page.locator('#reportedTable').count());
    console.log('resolvedTable count', await page.locator('#resolvedTable').count());
    await page.goto(`${BASE_URL}/reports/`, { waitUntil: 'networkidle' });
    console.log('/reports url', page.url());
    console.log('searchInput count', await page.locator('#searchInput').count());
  } catch (error) {
    console.error(error);
  } finally {
    await browser.close();
  }
})();