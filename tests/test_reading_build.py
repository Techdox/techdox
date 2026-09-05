"""Static output regressions. Python 3.11+ stdlib only; BLOG_BUILD selects build."""
import os
from pathlib import Path
import re
import unittest

BUILD = Path(os.environ.get('BLOG_BUILD', '/tmp/techdox-blog-build'))

def html(path='index.html'):
    return (BUILD / path).read_text()

class Build(unittest.TestCase):
    def test_editorial_cards(self):
        home = html()
        self.assertNotIn('class=card-term', home)
        self.assertIn('Privacy is not about disappearing', home)
        self.assertIn('class=term-hero', home)

    def test_one_article_title(self):
        for page in BUILD.glob('*/index.html'):
            text = page.read_text()
            if 'class=post-head' in text:
                with self.subTest(page=page.parent.name):
                    self.assertEqual(len(re.findall(r'<h1[ >]', text)), 1)

    def test_paginated_archive_is_compact(self):
        archive = html('page/2/index.html')
        self.assertNotIn('class=term-hero', archive)
        self.assertIn('Blog archive', archive)

    def test_article_social_cards(self):
        urls = []
        for slug in ('i-dont-want-to-be-the-product', 'kubesolo-moving-from-docker-to-kubernetes-in-a-homelab'):
            text = html(slug + '/index.html')
            url = re.search(r'<meta property="og:image" content="([^"]+)"', text).group(1)
            self.assertNotIn('og-default.png', url)
            from urllib.parse import urlparse
            png = (BUILD / urlparse(url).path.lstrip('/')).read_bytes()
            self.assertEqual(png[:8], b'\x89PNG\r\n\x1a\n')
            urls.append(url)
        self.assertNotEqual(*urls)

    def test_public_icons(self):
        self.assertTrue((BUILD / 'favicon.ico').exists(), 'Browser fallback favicon must exist')
        self.assertEqual((BUILD / 'favicon.ico').read_bytes()[:4], b'\x00\x00\x01\x00')
        self.assertTrue((BUILD / 'favicon.svg').exists())
        self.assertIn('favicon.svg', html())

    def test_related_label(self):
        self.assertIn('Related reading</h2>', html('i-dont-want-to-be-the-product/index.html'))

if __name__ == '__main__':
    unittest.main()
