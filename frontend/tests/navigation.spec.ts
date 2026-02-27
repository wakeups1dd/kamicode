import { test, expect } from '@playwright/test';

test.describe('Navigation', () => {
    test('should navigate to all core pages', async ({ page }) => {
        // Start at dashboard
        await page.goto('/');
        await expect(page.locator('h1')).toContainText(/Master/);

        // Go to Rush Mode
        await page.click('a[href="/rush"]');
        await expect(page).toHaveURL(/\/rush/);
        await expect(page.locator('h1')).toContainText(/Rapid Rush/i);

        // Go to Leaderboards
        await page.click('a[href="/leaderboards"]');
        await expect(page).toHaveURL(/\/leaderboards/);
        await expect(page.locator('h1')).toContainText(/Fame/i);

        // Check Profile navigation
        await page.click('a[href="/profile"]');
        await expect(page).toHaveURL(/\/profile/);
        await expect(page.locator('h1')).toContainText(/Master/i);
    });
});
