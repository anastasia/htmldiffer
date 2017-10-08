import unittest
from .fixtures import *
from htmldiffer.utils import *
from htmldiffer import settings


class TestUtilMethods(unittest.TestCase):
    def test_tokenize_html(self):
        html_str = "<h1>This is a simple header</h1>"
        result = list(tokenize_html(html_str))
        self.assertEqual(result, ['<h1>', 'This ', 'is ', 'a ', 'simple ', 'header', '</h1>'])
        self.assertEqual(''.join(result), html_str)

        # test blacklisted
        settings.BLACKLISTED_TAGS = ['head']
        html_str = "<head><title>Page Title</title></head>"
        result = list(tokenize_html(html_str))
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

    def test_is_complete_tag_block(self):
        self.assertTrue(is_complete_tag_block('script', script_str))
        self.assertTrue(is_complete_tag_block('div', div_tag))
        self.assertTrue(is_complete_tag_block('span', span_tag))
        self.assertTrue(is_complete_tag_block('img', img_tag))

        incomplete_tag = "<head class='some_class hey'>hey there</head"
        self.assertFalse(is_complete_tag_block('head', incomplete_tag))
        incomplete_tag = "<head class='some_class hey'>hey there<script>script_goes_here</script></head"
        self.assertFalse(is_complete_tag_block('head', incomplete_tag))

    def test_is_text(self):
        print("testing test_is_text")
        self.assertTrue(is_text("hello!"))
        self.assertTrue(is_text("hello>"))
        self.assertFalse(is_text("<area>"))
        self.assertFalse(is_text("<area class='some class'>hi"))

def main():
    unittest.main()

if __name__ == '__main__':
    main()
