import unittest
from .fixtures import *
from htmldiffer.utils import *
from htmldiffer import settings

class TestUtilMethods(unittest.TestCase):
    def test_html2diff(self):
        html_str = "<h1>This is a simple header</h1>"
        result = html2list(html_str)
        self.assertEqual(result, ['<h1>', 'This ', 'is ', 'a ', 'simple ', 'header', '</h1>'])

        settings.BLACKLISTED_TAGS = ['head']
        html_str = "<head><title>Page Title</title></head>"
        result = html2list(html_str)
        self.assertEqual(result, ['<head><title>Page Title</title></head>'])

    def test_is_whitelisted_tag(self):
        self.assertTrue(is_whitelisted_tag(img_tag))
        self.assertFalse(is_whitelisted_tag(div_tag))
        self.assertFalse(is_whitelisted_tag(span_tag))

        settings.WHITELISTED_TAGS.append('span')
        self.assertTrue(is_whitelisted_tag(span_tag))
        settings.WHITELISTED_TAGS.pop()


def main():
    unittest.main()

if __name__ == '__main__':
    main()
