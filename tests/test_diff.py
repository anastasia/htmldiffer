import unittest
from htmldiff.diff import *
from htmldiff import settings
from fixtures import *

class TestDiffMethods(unittest.TestCase):
    def test_wrap_text(self):
        list_to_wrap = ['<a>', 'b', 'c ', '</a>']
        wrapped_str = wrap_text('insert', list_to_wrap)

        list_to_wrap = ['<a>', 'b is for boy', '<div>', 'c is for cat','</div>', 'd is for dongle ', '</a>']
        wrapped_str = wrap_text('insert', list_to_wrap)
        self.assertEqual(wrapped_str, '<a><span class="diff_insert">b is for boy</span><div><span class="diff_insert">c is for cat</span></div><span class="diff_insert">d is for dongle </span></a>')

    def test_add_style_str(self):
        html_list = html2list(html_str)
        new_html_list = add_style_str(html_list)
        self.assertNotEqual(new_html_list[1], '</head>')

        new_html_string = "".join(new_html_list)
        self.assertTrue('</style></head>' in new_html_string)
        self.assertTrue('span.diff_insert' in new_html_string)

        html_list = html2list(html_str)
        settings.CUSTOM_STYLE_STR = "<style>span.diff_insert {text-decoration: underline; color: green;} span.diff_delete {color: red;}</style>"
        custom_styled_list = add_style_str(html_list)
        custom_styled_string = "".join(custom_styled_list)
        self.assertTrue("background-color" not in custom_styled_string)
        self.assertTrue(settings.CUSTOM_STYLE_STR in custom_styled_string)

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
        out = text_diff(script_str, script_str_2)

        self.assertEqual(out[0], script_str)
        self.assertEqual(out[1], script_str_2)

        out = text_diff(script_str_3, script_str_4)
        self.assertFalse(out[0] == script_str_3)
        self.assertFalse(out[1] == script_str_4)

        self.assertTrue("diff_delete" in out[0])
        self.assertTrue("diff_insert" in out[1])


def main():
    unittest.main()

if __name__ == '__main__':
    main()
