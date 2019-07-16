import unittest
from .fixtures import *
from htmldiffer.utils import *
from htmldiffer import settings


class TestUtilMethods(unittest.TestCase):
    def test_html2diff(self):
        html_str = "<h1>This is a simple header</h1>"
        result = html2list(html_str)
        self.assertEqual(result, ['<h1>', 'This', ' ', 'is', ' ', 'a', ' ', 'simple', ' ', 'header', '</h1>'])

        settings.BLACKLISTED_TAGS = ['head']
        html_str = "<head><title>Page Title</title></head>"
        result = html2list(html_str)
        self.assertEqual(result, ['<head><title>Page Title</title></head>'])

    def test_is_whitelisted_tag(self):
        img_tagname = extract_tagname(img_tag)
        self.assertTrue(is_whitelisted_tag(img_tagname))
        div_tagname = extract_tagname(div_tag)
        self.assertFalse(is_whitelisted_tag(div_tagname))
        span_tagname = extract_tagname(span_tag)
        self.assertFalse(is_whitelisted_tag(span_tagname))

    def test_chart_tag(self):
        tag_string = '<div title="elsewhere">'
        tag_parts = chart_tag(tag_string)
        self.assertEqual(tag_parts['tag'], 'div')
        self.assertEqual(tag_parts['title'], 'elsewhere')

        tag_string = '<input name="q" type="text" placeholder="Search..." value="" tabindex="1" autocomplete="off" maxlength="240" class="f-input js-search-field">'
        tag_parts = chart_tag(tag_string)
        self.assertEqual(tag_parts['tag'], 'input')
        self.assertEqual(tag_parts['placeholder'], 'Search...')
        # make sure we capture multiple class values
        self.assertEqual(tag_parts['class'], 'f-input js-search-field')

    def test_extract_tagname(self):
        tag_name = extract_tagname(img_tag)
        self.assertEqual(tag_name, 'img')

        tag_name = extract_tagname(div_tag)
        self.assertEqual(tag_name, 'div')

        tag_name = extract_tagname(span_tag)
        self.assertEqual(tag_name, 'span')

        with self.assertRaises(Exception):
            extract_tagname("not a tag")

        tag_name = extract_tagname(script_str)
        self.assertEqual(tag_name, 'script')

def main():
    unittest.main()

if __name__ == '__main__':
    main()
