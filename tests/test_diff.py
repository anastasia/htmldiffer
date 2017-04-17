import unittest
import re
from htmldiff.diff import *
from fixtures import *

class TestDiffMethods(unittest.TestCase):
    def test_html2list(self):
        html_list = html2list(html_str, ignore_head_changes=True)
        self.assertTrue("</head>" in html_list[0])
        self.assertFalse("</head>" in html_list[1])
        self.assertTrue('class="this_is_a_class"' in html_list[0])

    def test_is_whitelisted_tag(self):
        self.assertTrue(is_whitelisted_tag(img_tag))
        self.assertFalse(is_whitelisted_tag(div_tag))

    def test_wrap_text(self):
        list_to_wrap = ['<a>', 'b', 'c ', '</a>']
        wrapped_str = wrap_text('insert', list_to_wrap)
        # self.assertEqual(wrapped_str, '<a><span class="diff_insert">bc </span></a>')

        list_to_wrap = ['<a>', 'b is for boy', '<div>', 'c is for cat','</div>', 'd is for dongle ', '</a>']
        wrapped_str = wrap_text('insert', list_to_wrap)
        self.assertEqual(wrapped_str, '<a><span class="diff_insert">b is for boy</span><div><span class="diff_insert">c is for cat</span></div><span class="diff_insert">d is for dongle </span></a>')

    def test_add_style_str(self):
        html_list = html2list(html_str, ignore_head_changes=True)
        new_html_list = add_style_str(html_list, style_str=None)
        self.assertNotEqual(new_html_list[1], '</head>')
        self.assertTrue('</head>' in new_html_list[0])
        self.assertTrue('span.diff_insert' in new_html_list[0])

        custom_style_str = "<style>span.diff_insert {text-decoration: underline; color: green;} span.diff_delete {color: red;}</style>"
        custom_styled_list = add_style_str(html_list, style_str=custom_style_str)

        self.assertTrue("background-color" not in custom_styled_list[0])
        self.assertTrue(custom_style_str in custom_styled_list[0])

    def test_text_diff(self):
        out = text_diff(html_str, html_different_str)

        # self.assertTrue((len(out[2]) > len(out[1])) and len(out[2]) > len(out[0]))

        self.assertEqual(out[0][-7:], '</html>')
        self.assertEqual(out[1][-7:], '</html>')
        self.assertEqual(out[2][-7:], '</html>')

        self.assertTrue('class="diff_delete"' in out[0])
        self.assertTrue('class="diff_insert"' in out[1])
        self.assertTrue('class="diff_insert"' in out[2] and 'class="diff_delete"' in out[2])

        self.assertFalse('class="diff_insert"' in out[0])
        self.assertFalse('class="diff_delete"' in out[1])

    def test_script_str(self):
        """script tags should be ignored"""
        out = text_diff(script_str, script_str_2, add_style=False, ignore_head_changes=False)
        self.assertEqual(out[0], script_str)
        self.assertEqual(out[1], script_str_2)

        out = text_diff(script_str_3, script_str_4, add_style=False, ignore_head_changes=False)
        self.assertFalse(out[0] == script_str_3)
        self.assertFalse(out[1] == script_str_4)

        self.assertTrue("diff_delete" in out[0])
        self.assertTrue("diff_insert" in out[1])


def main():
    unittest.main()

if __name__ == '__main__':
    main()
