import unittest
import re
from diff import *
from fixtures import html_str, html_different_str, img_tag, div_tag

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

        list_to_wrap = ['<a>', 'b is for boy', '<div>', 'c is for cat','</div>', 'd is for dongle ', '</a>']
        wrapped_str = wrap_text('insert', list_to_wrap)
        self.assertEqual(wrapped_str, '<a><span class="diff_insert">b is for boy</span><div><span class="diff_insert">c is for cat</span></div><span class="diff_insert">d is for dongle </span></a>')

    def test_add_style_str(self):
        html_list = html2list(html_str)
        self.assertEqual(html_list[1], '</head>')

        new_html_list = add_style_str(html_list)
        self.assertNotEqual(new_html_list[1], '</head>')
        self.assertTrue('</head>' in new_html_list[0])
        self.assertTrue('span.diff_insert' in new_html_list[0])

    def test_text_diff(self):
        out = text_diff(html_str, html_different_str)
        self.assertTrue((len(out[2]) > len(out[1])) and len(out[2]) > len(out[0]))

        self.assertEqual(out[0][-7:], '</html>')
        self.assertEqual(out[1][-7:], '</html>')
        self.assertEqual(out[2][-7:], '</html>')

        self.assertTrue('class="diff_delete"' in out[0])
        self.assertTrue('class="diff_insert"' in out[1])
        self.assertTrue('class="diff_insert"' in out[2] and 'class="diff_delete"' in out[2])

        self.assertFalse('class="diff_insert"' in out[0])
        self.assertFalse('class="diff_delete"' in out[1])

def main():
    unittest.main()

if __name__ == '__main__':
    main()
