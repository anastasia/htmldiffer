import unittest
from htmldiff import settings
from fixtures import *
from htmldiff.utils import *

class TestUtilMethods(unittest.TestCase):
    def test_html2list(self):
        html_list = html2list(html_str)
        self.assertTrue("</head>" in html_list[0])
        self.assertFalse("</head>" in html_list[1])
        self.assertTrue('class="this_is_a_class"' in html_list[0])

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
