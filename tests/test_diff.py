import unittest
import tempfile
from htmldiffer.diff import *
from htmldiffer import settings
from .fixtures import *


class TestDiffMethods(unittest.TestCase):
    def test_wrap_text(self):
        list_to_wrap = ['<a>', 'b', 'c ', '</a>']
        wrapped_str = wrap_text('insert', list_to_wrap)
        self.assertEqual(wrapped_str, '<a><span class="diff_insert">b</span><span class="diff_insert">c </span></a>')

        list_to_wrap = ['<a>', 'b is for boy', '<div>', 'c is for cat','</div>', 'd is for dongle ', '</a>']
        wrapped_str = wrap_text('insert', list_to_wrap)
        self.assertEqual(wrapped_str, '<a><span class="diff_insert">'
                                      'b is for boy</span><div><span class="diff_insert">'
                                      'c is for cat</span></div><span class="diff_insert">'
                                      'd is for dongle </span></a>')

    def test_add_style_str(self):
        """Test adding style string and custom style string to <head> of the html stirng"""
        html_list = html2list(html_str)
        new_html_list = add_style_str(html_list)
        self.assertNotEqual(new_html_list[1], '</head>')

        new_html_string = "".join(new_html_list)
        self.assertTrue('</style></head>' in new_html_string)
        self.assertTrue('span.diff_insert' in new_html_string)

        html_list = html2list(html_str)
        custom_style_str = "<style>span.diff_insert {text-decoration: underline; color: green;} span.diff_delete {color: red;}</style>"
        custom_styled_list = add_style_str(html_list, custom_style_str=custom_style_str)
        custom_styled_string = "".join(custom_styled_list)
        self.assertTrue("background-color" not in custom_styled_string)
        self.assertTrue(settings.CUSTOM_STYLE_STR in custom_styled_string)

    def test_differ_with_strings(self):
        result = HTMLDiffer(html_str, html_different_str)

        self.assertEqual(result.deleted_diff[-7:], '</html>')
        self.assertEqual(result.inserted_diff[-7:], '</html>')
        self.assertEqual(result.combined_diff[-7:], '</html>')

        self.assertTrue('class="diff_delete"' in result.deleted_diff)
        self.assertTrue('class="diff_insert"' in result.inserted_diff)
        self.assertTrue('class="diff_insert"' in result.combined_diff and 'class="diff_delete"' in result.combined_diff)

        self.assertFalse('class="diff_insert"' in result.deleted_diff)
        self.assertFalse('class="diff_delete"' in result.inserted_diff)

    def test_differ_with_files(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp1:
            tmp1.write(html_str.encode())

        with tempfile.NamedTemporaryFile(delete=False) as tmp2:

            tmp2.write(html_different_str.encode())

        result = HTMLDiffer(tmp1.name, tmp2.name)

        self.assertTrue('class="diff_delete"' in result.deleted_diff)
        self.assertTrue('class="diff_insert"' in result.inserted_diff)
        self.assertTrue('class="diff_insert"' in result.combined_diff and 'class="diff_delete"' in result.combined_diff)

    def test_differ_with_both_string_and_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp1:
            tmp1.write(html_str.encode())

        result = HTMLDiffer(tmp1.name, html_different_str)

        self.assertTrue('class="diff_delete"' in result.deleted_diff)
        self.assertTrue('class="diff_insert"' in result.inserted_diff)
        self.assertTrue('class="diff_insert"' in result.combined_diff and 'class="diff_delete"' in result.combined_diff)

    def test_script_str(self):
        """script tags should be ignored"""
        result = HTMLDiffer(script_str, script_str_2)

        self.assertEqual(result.deleted_diff, script_str)
        self.assertEqual(result.inserted_diff, script_str_2)

        result = HTMLDiffer(script_str_3, script_str_4)
        self.assertFalse(result.deleted_diff == script_str_3)
        self.assertFalse(result.inserted_diff == script_str_4)

        self.assertTrue("diff_delete" in result.deleted_diff)
        self.assertTrue("diff_insert" in result.inserted_diff)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
