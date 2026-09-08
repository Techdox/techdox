"""Brand browser regressions, discovered by scripts/test.py alongside reading tests."""
import json
import os
from pathlib import Path
import unittest
from playwright.sync_api import sync_playwright

BASE = os.environ.get('BLOG_TEST_URL', 'http://localhost:8766')
TUTORIAL = '/kubesolo-moving-from-docker-to-kubernetes-in-a-homelab/'

class BrandBrowser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch(executable_path=os.environ.get('BROWSER_EXECUTABLE'))

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def test_identity_themes_fonts_and_clearspace(self):
        evidence = os.environ.get('BLOG_EVIDENCE')
        metrics = []
        for width in (320, 390, 768, 1440):
            page = self.browser.new_page(viewport={'width': width, 'height': 1000})
            page.route('https://umami.techdox.nz/**', lambda route: route.abort())
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            for theme in ('dark', 'light'):
                page.goto(BASE + TUTORIAL)
                if page.locator('html').get_attribute('data-theme') != theme:
                    page.locator('#theme').click()
                page.reload()
                page.evaluate('document.fonts.ready')
                page.wait_for_timeout(450)
                self.assertEqual(page.locator('html').get_attribute('data-theme'), theme)
                self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'), width)
                self.assertIn('Fraunces', page.locator('.post-head h1').evaluate('(e) => getComputedStyle(e).fontFamily'))
                self.assertIn('Hanken Grotesk', page.locator('body').evaluate('(e) => getComputedStyle(e).fontFamily'))
                self.assertIn('JetBrains Mono', page.locator('.prose pre code').first.evaluate('(e) => getComputedStyle(e).fontFamily'))
                loaded = page.evaluate("Array.from(document.fonts).filter(f => f.status === 'loaded').map(f => f.family.replaceAll('\"',''))")
                for family in ('Fraunces', 'Hanken Grotesk', 'JetBrains Mono'):
                    self.assertIn(family.lower(), [name.lower() for name in loaded])
                for brand in page.locator('.brand').all():
                    image = brand.locator('.brand-' + theme)
                    self.assertTrue(image.is_visible())
                    self.assertFalse(brand.locator('.brand-' + ('light' if theme == 'dark' else 'dark')).is_visible())
                    data = image.evaluate('''async img => {
                      const text = await (await fetch(img.src)).text();
                      const host = document.createElement('div');
                      host.style.cssText = 'position:fixed;left:-10000px';
                      host.innerHTML = text; document.body.append(host);
                      const svg = host.firstElementChild, b = svg.getBBox();
                      const fill = [...svg.querySelectorAll('g')].map(g => g.getAttribute('fill'));
                      const r = img.getBoundingClientRect(), mark = img.parentElement.getBoundingClientRect();
                      const scale = r.width / svg.viewBox.baseVal.width;
                      const visible = {x:r.x+b.x*scale, y:r.y+b.y*scale, width:b.width*scale, height:b.height*scale};
                      const padding = getComputedStyle(img.closest('.brand'));
                      const result = {visible, fill, mark:{x:mark.x,y:mark.y,width:mark.width,height:mark.height}, padding:parseFloat(padding.paddingTop), animation:getComputedStyle(img).animationName};
                      host.remove(); return result;
                    }''')
                    v, m = data['visible'], data['mark']
                    self.assertGreaterEqual(v['width'], 140)
                    self.assertGreaterEqual(data['padding'], m['height']/2)
                    self.assertGreaterEqual(v['x'], m['x'])
                    self.assertGreaterEqual(v['y'], m['y'])
                    self.assertLessEqual(v['x']+v['width'], m['x']+m['width'])
                    self.assertLessEqual(v['y']+v['height'], m['y']+m['height'])
                    self.assertEqual(data['animation'], 'none')
                    self.assertIn('#f4f7fb' if theme == 'dark' else '#090c12', data['fill'])
                    metrics.append({'width':width, 'theme':theme, **data})
                # Primary CTA and body/secondary text must pass AA in both themes.
                ratios = page.evaluate('''() => {
                  const c = getComputedStyle(document.documentElement);
                  const lum = hex => {const rgb=hex.trim().replace('#',''); return [0,2,4].map(i=>parseInt(rgb.length===3?rgb[i/2].repeat(2):rgb.slice(i,i+2),16)/255).map(x=>x<=.04045?x/12.92:((x+.055)/1.055)**2.4).reduce((s,x,i)=>s+x*[.2126,.7152,.0722][i],0)};
                  return [['--text','--bg'],['--muted','--panel'],['--faint','--panel-2'],['--accent','--bg'],['--on-accent','--accent']].map(([a,b])=>{const x=lum(c.getPropertyValue(a)),y=lum(c.getPropertyValue(b));return {a,b,ratio:(Math.max(x,y)+.05)/(Math.min(x,y)+.05)}});
                }''')
                self.assertTrue(all(r['ratio'] >= 4.5 for r in ratios), ratios)
                if evidence and width in (390,1440):
                    page.screenshot(path=str(Path(evidence) / f'article-{width}-{theme}.png'), full_page=True)
                    page.goto(BASE)
                    page.evaluate('document.fonts.ready')
                    page.wait_for_timeout(1600)
                    page.screenshot(path=str(Path(evidence) / f'home-{width}-{theme}.png'), full_page=True)
                self.assertEqual(errors, [])
            page.close()
        if evidence:
            (Path(evidence) / 'brand-browser-metrics.json').write_text(json.dumps(metrics, indent=2))

if __name__ == '__main__':
    unittest.main()
