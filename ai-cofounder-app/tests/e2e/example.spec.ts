import { test, expect } from '@playwright/test';

test('should load homepage', async ({ page }) => {
  await page.goto('/');
  
  await expect(page).toHaveTitle(/AI Cofounder/);
  
  const heading = page.getByRole('heading', { name: /AI Cofounder/i });
  await expect(heading).toBeVisible();
});

test('should have working navigation', async ({ page }) => {
  await page.goto('/');
  
  // Test navigation exists
  const nav = page.getByRole('navigation');
  await expect(nav).toBeVisible();
});
