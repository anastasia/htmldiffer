import unittest
import re
from diff import *
from fixtures import html_str, img_tag, div_tag

class TestDiffMethods(unittest.TestCase):
    def test_html2list(self):
        html_list = html2list(html_str)
        self.assertEqual(html_list[1], "</head>")
        self.assertFalse("</head>" in html_list[2])
        self.assertTrue('class="this_is_a_class"' in html_list[0])

        """test if the two strings are functionally the same"""
        new_html_string = "".join(html_list)
        rx = re.compile('\n|\t|\r|\s{2}')
        original_html_string = html_str
        original_html_string = rx.sub('', original_html_string)

        # TODO: make sure that a space before text does not make a difference in html, ever
        self.assertTrue("test <b>" in new_html_string)
        self.assertFalse("<div> test " in new_html_string)
        self.assertTrue("<div>test " in new_html_string)

        new_html_list = html2list(new_html_string)
        self.assertEqual(new_html_list, html_list)

    def test_is_whitelisted_tag(self):
        self.assertTrue(is_whitelisted_tag(img_tag))
        self.assertFalse(is_whitelisted_tag(div_tag))

    def test_wrap_text(self):
        list_to_wrap = ['<a>', 'b', 'c ', '</a>']
        wrapped_str = wrap_text('insert', list_to_wrap)
        self.assertEqual(wrapped_str, '<a><span class="diff_insert">bc </span></a>')

def main():
    unittest.main()

if __name__ == '__main__':
    main()
