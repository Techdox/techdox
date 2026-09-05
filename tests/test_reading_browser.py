"""Run against a Hugo build served at BLOG_TEST_URL (default localhost:8766).
Requires Playwright with Chromium; BROWSER_EXECUTABLE optionally selects binary.
"""
import os
import unittest
from playwright.sync_api import sync_playwright

BASE = os.environ.get('BLOG_TEST_URL', 'http://localhost:8766')
TUTORIAL = '/kubesolo-moving-from-docker-to-kubernetes-in-a-homelab/'

class Reading(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch(executable_path=os.environ.get('BROWSER_EXECUTABLE'))

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def setUp(self):
        self.page = self.browser.new_page()
        self.page.route('https://umami.techdox.nz/**', lambda r: r.abort())

    def tearDown(self):
        self.page.close()

    def test_mobile_overflow(self):
        for width in (320, 375, 390):
            self.page.set_viewport_size({'width': width, 'height': 850})
            for path in ('/', TUTORIAL):
                with self.subTest(width=width, path=path):
                    self.page.goto(BASE + path)
                    self.page.evaluate('document.fonts.ready')
                    self.page.wait_for_timeout(1600)
                    self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'), width)
                    if path == '/':
                        self.assertFalse(self.page.locator('.feat-term').evaluate('(e) => e.getBoundingClientRect().right > innerWidth'), 'Featured terminal must fit, not be silently clipped')
                    if path == TUTORIAL:
                        self.assertEqual(self.page.locator('.prose pre').first.evaluate('(e) => getComputedStyle(e).overflowX'), 'auto')

    def test_copy_code_and_failure(self):
        self.page.context.grant_permissions(['clipboard-read', 'clipboard-write'])
        self.page.goto(BASE + TUTORIAL)
        self.assertEqual(self.page.get_by_role('button', name='Copy code', exact=True).count(), self.page.locator('.prose pre').count())
        button = self.page.get_by_role('button', name='Copy code', exact=True).first
        expected = self.page.locator('.prose pre code').first.inner_text()
        button.click()
        self.page.wait_for_function("document.querySelector('.copy-status')?.textContent === 'Copied.'")
        self.assertEqual(self.page.evaluate('navigator.clipboard.readText()'), expected)
        self.page.evaluate("Object.defineProperty(navigator, 'clipboard', {value: {writeText: () => Promise.reject(new Error('Denied'))}, configurable:true})")
        button.click()
        self.page.wait_for_function("document.querySelector('.copy-status')?.textContent.includes('Select')")

    def test_search_and_navigation(self):
        self.page.goto(BASE + '/search/')
        self.assertEqual(self.page.get_by_role('searchbox', name='Search posts').count(), 1, 'Search page needs a labelled search field')
        self.page.get_by_role('searchbox', name='Search posts').fill('kubesolo')
        self.page.wait_for_function("document.querySelector('#search-status')?.textContent.includes('result')")
        self.assertTrue(self.page.locator('#search-results a').filter(has_text='KubeSolo').first.is_visible())
        self.page.get_by_role('searchbox', name='Search posts').fill('zzzz-nothing-matches-12345')
        self.page.wait_for_function("document.querySelector('#search-status')?.textContent.includes('No posts')")
        self.assertEqual(self.page.locator('#search-results a').count(), 0)
        self.assertTrue(self.page.locator('nav a[href="https://techdox.nz/"]').is_visible())
        self.page.keyboard.press('Control+Home')

    def test_metadata_contrast_in_both_themes(self):
        self.page.goto(BASE)
        for theme in ('dark', 'light'):
            self.page.evaluate('(theme) => document.documentElement.dataset.theme = theme', theme)
            self.page.wait_for_timeout(400)
            ratios = self.page.locator('.meta, .sh-num').evaluate_all('''elements => elements.map(e => {
              const parse = c => c.match(/[\\d.]+/g).map(Number);
              let parent = e, bg;
              do { bg = parse(getComputedStyle(parent).backgroundColor); parent = parent.parentElement; }
              while (parent && bg[3] === 0);
              const fg = parse(getComputedStyle(e).color);
              const alpha = fg[3] ?? 1;
              const blend = fg.slice(0,3).map((c,i) => c*alpha + bg[i]*(1-alpha));
              const luminance = rgb => rgb.slice(0,3).map(c => c/255).map(c => c<=.04045 ? c/12.92 : ((c+.055)/1.055)**2.4).reduce((sum,c,i) => sum+c*[.2126,.7152,.0722][i],0);
              const a=luminance(blend), b=luminance(bg);
              return (Math.max(a,b)+.05)/(Math.min(a,b)+.05);
            })''')
            self.assertTrue(ratios and min(ratios) >= 4.5, (theme, ratios))

    def test_reduced_motion_keeps_terminal_text_visible(self):
        self.page.emulate_media(reduced_motion='reduce')
        self.page.goto(BASE)
        self.assertTrue(self.page.locator('.term-line').evaluate_all("items => items.every(e => getComputedStyle(e).opacity === '1' && getComputedStyle(e).animationName === 'none')"))

    def test_start_here_sequence(self):
        self.page.goto(BASE)
        titles = self.page.locator('.sh-title').all_text_contents()
        self.assertEqual(titles[:2], ['Why Selfhost?', 'Why Linux For Selfhosting?'])
        self.assertIn('Raspberry Pi', titles[2])
        self.assertIn('KubeSolo', titles[3])
        self.assertIn('Optional', self.page.locator('.sh-item').last.inner_text())
        self.page.set_viewport_size({'width': 320, 'height': 850})
        self.assertEqual(self.page.locator('.sh-title').first.evaluate('(e) => getComputedStyle(e).whiteSpace'), 'normal')

if __name__ == '__main__':
    unittest.main()
