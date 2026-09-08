"""Brand output regressions; BLOG_BUILD selects a minified production build."""
import os
from pathlib import Path
import re
import unittest

BUILD = Path(os.environ.get('BLOG_BUILD', '/tmp/techdox-blog-build'))

class Brand(unittest.TestCase):
    def test_dark_palette_and_light_adaptation(self):
        css = next((BUILD / 'css').glob('main*.css')).read_text().lower()
        for token, value in {'bg':'#090c12', 'bg-soft':'#0d121b', 'panel':'#111824', 'panel-2':'#151e2c', 'text':'#f4f7fb', 'muted':'#9aa8bc', 'faint':'#9aa8bc', 'accent':'#4d8dff', 'accent-bright':'#79aaff', 'border':'#293445'}.items():
            self.assertRegex(css, '--' + token + r'\s*:\s*' + value)
        self.assertRegex(css, r'--bg\s*:\s*#f6f5f1')
        self.assertRegex(css, r'--accent\s*:\s*#1958d7')
        self.assertRegex(css, r'--on-accent\s*:\s*#090c12')
        self.assertIn('fraunces-latin.woff2', css)
        self.assertIn('hanken-latin.woff2', css)
        self.assertIn('jetbrains-latin.woff2', css)

    def test_brand_icons_and_generic_social_fallback(self):
        import json
        from html.parser import HTMLParser
        class Tags(HTMLParser):
            def __init__(self, text):
                super().__init__(); self.tags = []; self.feed(text)
            def handle_starttag(self, tag, attrs):
                self.tags.append((tag, dict(attrs)))
        for path in ('index.html', 'posts/index.html', 'tags/index.html', 'search/index.html', '404.html', 'page/2/index.html'):
            tags = Tags((BUILD / path).read_text()).tags
            for key in ('og:image', 'twitter:image'):
                meta = next(a for t,a in tags if t == 'meta' and (a.get('property') == key or a.get('name') == key))
                self.assertEqual(meta['content'], 'https://blog.techdox.nz/og-default.png')
            self.assertTrue(any(t == 'link' and a.get('rel') == 'apple-touch-icon' for t,a in tags))
            self.assertTrue(any(t == 'link' and a.get('rel') == 'manifest' for t,a in tags))
        manifest = json.loads((BUILD / 'site.webmanifest').read_text())
        self.assertEqual(manifest['start_url'], '/')
        self.assertEqual(manifest['background_color'], '#090c12')
        for icon in manifest['icons']:
            self.assertTrue((BUILD / icon['src'].lstrip('/')).is_file())
        # Exact copies, not reconstructed artwork. Hashes recorded from the kit.
        import hashlib
        expected = json.loads((Path(__file__).parent / 'brand-assets.json').read_text())
        for path, digest in expected.items():
            self.assertTrue((BUILD / path).is_file(), path + ' must be distributed')
            self.assertEqual(hashlib.sha256((BUILD / path).read_bytes()).hexdigest(), digest, path)

    def test_article_image_precedence(self):
        from html.parser import HTMLParser
        class Metadata(HTMLParser):
            def __init__(self, text):
                super().__init__(); self.values = {}; self.feed(text)
            def handle_starttag(self, tag, attrs):
                a = dict(attrs)
                if tag == 'meta':
                    self.values[a.get('property', a.get('name'))] = a.get('content')
        import tomllib
        from urllib.parse import urljoin
        root = Path(__file__).resolve().parents[1]
        posts = {}
        for source in (root / 'content/posts').glob('*.md'):
            if source.name == '_index.md':
                continue
            data = tomllib.loads(source.read_text().split('+++')[1])
            if not data.get('draft'):
                posts[data['title']] = data
        checked = set()
        for page in BUILD.glob('*/index.html'):
            text = page.read_text()
            if 'class=post-head' not in text:
                continue
            meta = Metadata(text).values
            title, image, twitter = meta['og:title'], meta['og:image'], meta['twitter:image']
            self.assertEqual(image, twitter)
            feature = posts[title].get('feature_image')
            if feature:
                self.assertEqual(image, urljoin('https://blog.techdox.nz/', feature))
            else:
                self.assertNotIn('og-default.png', image)
                self.assertIn('/images/social-base_', image)
            checked.add(title)
        self.assertEqual(checked, set(posts))

    def test_site_descriptor(self):
        home = (BUILD / 'index.html').read_text()
        self.assertIn('name=description content="Practical self-hosting, from my own homelab."', home)
        self.assertNotIn('Your fun and informative source for IT goodness.', home)
        self.assertIn('Practical self-hosting, from my own homelab.</p>', home)

    def test_supplied_wordmarks(self):
        home = (BUILD / 'index.html').read_text()
        for name in ('primary-dark.svg', 'primary-light.svg'):
            self.assertIn('/brand/' + name, home)
            svg = (BUILD / 'brand' / name).read_text()
            self.assertNotIn('<text', svg)
            self.assertNotIn('<animate', svg)
        self.assertNotIn('class=cursor', home)
        self.assertIn('aria-label="Techdox home"', home)
        self.assertIn('aria-label="Techdox blog home"', home)

if __name__ == '__main__':
    unittest.main()
