import subprocess
import unittest
import tempfile
from htmldiffer.diff import *
from htmldiffer import utils
from tests.fixtures import *

tag_change_class_delete = utils.get_class_decorator("tag_change", "delete")
tag_change_class_insert = utils.get_class_decorator("tag_change", "insert")
insert_class = utils.get_class_decorator("change", "insert")
delete_class = utils.get_class_decorator("change", "delete")
combined_class = utils.get_class_decorator("change", "change")


class TestDiffMethods(unittest.TestCase):
    def test_wrap_text(self):
        list_to_wrap = ['<a>', 'b', 'c ', '</a>']
        wrapped_str = wrap_text('insert', list_to_wrap)
        self.assertEqual(wrapped_str, '<a class="{0}"><span class="{1}">b</span><span class="{1}">c </span></a>'.format(tag_change_class_insert, insert_class))

        list_to_wrap = ['<a>', 'b is for boy', '<div>', 'c is for cat',
                        '</div>', 'd is for dongle ', '</a>']
        wrapped_str = wrap_text('insert', list_to_wrap)
        # self.assertEqual(wrapped_str, '<a  class="{0}"><span class="{1}">'\
        #                               'b is for boy</span><div><span class="{1}">'\
        #                               'c is for cat</span></div><span class="{1}">'\
        #                               'd is for dongle </span></a>'.format(tag_change_class_insert, insert_class))

    def test_add_stylesheet(self):
        """Test adding style string and custom style string to <head> of the html string"""
        html_list = utils.html2list(html_str)
        new_html_list = utils.add_stylesheet(html_list)
        self.assertNotEqual(new_html_list[1], '</head>')
        new_html_string = "".join(new_html_list)
        self.assertTrue('.css\"></head>' in new_html_string)
        self.assertTrue('<link rel="stylesheet"' in new_html_string)

    def test_differ_with_strings(self):
        result = HTMLDiffer(html_str, html_different_str)

        self.assertEqual(result.deleted_diff.strip()[-7:], '</html>')
        self.assertEqual(result.inserted_diff.strip()[-7:], '</html>')
        self.assertEqual(result.combined_diff.strip()[-7:], '</html>')

        self.assertTrue('class="{}"'.format(insert_class) in result.inserted_diff)
        self.assertTrue('class="{}"'.format(delete_class) in result.deleted_diff)

        self.assertTrue('class="{}"'.format(insert_class) in result.combined_diff)
        self.assertTrue('class="{}"'.format(delete_class) in result.combined_diff)

        self.assertFalse('class="{}"'.format(insert_class) in result.deleted_diff)
        self.assertFalse('class="{}"'.format(delete_class) in result.inserted_diff)

    def test_differ_with_files(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp1:
            tmp1.write(html_str.encode())

        with tempfile.NamedTemporaryFile(delete=False) as tmp2:

            tmp2.write(html_different_str.encode())

        result = HTMLDiffer(tmp1.name, tmp2.name)

        self.assertTrue('class="{}"'.format(delete_class) in result.deleted_diff)
        self.assertTrue('class="{}"'.format(insert_class) in result.inserted_diff)

        self.assertTrue('class="{}"'.format(delete_class) in result.combined_diff)
        self.assertTrue('class="{}"'.format(insert_class) in result.combined_diff)


    def test_differ_with_both_string_and_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp1:
            tmp1.write(html_str.encode())

        result = HTMLDiffer(tmp1.name, html_different_str)

        self.assertTrue('class="{}"'.format(delete_class) in result.deleted_diff)
        self.assertTrue('class="{}"'.format(insert_class) in result.inserted_diff)
        # combined diff has both classes
        self.assertTrue('class="{}"'.format(delete_class) in result.combined_diff)
        self.assertTrue('class="{}"'.format(insert_class) in result.combined_diff)

    def test_script_str(self):
        """script tags should be ignored"""
        result = HTMLDiffer(script_str, script_str_2)

        self.assertEqual(result.deleted_diff, script_str)
        self.assertEqual(result.inserted_diff, script_str_2)

        result = HTMLDiffer(script_str_3, script_str_4)
        self.assertFalse(result.deleted_diff == script_str_3)
        self.assertFalse(result.inserted_diff == script_str_4)

        self.assertTrue(delete_class in result.deleted_diff)
        self.assertTrue(insert_class in result.inserted_diff)

    def test_add_diff_class(self):
        """ returns out if closing tag"""
        tag = "</script>"
        marked_up_tag = add_diff_class("delete", tag)
        self.assertEqual(marked_up_tag, tag)
        # change that two classes (insert and delete)
        # will be added to the combined diff
        # in case of an attribute change
        combined_diff = HTMLDiffer(href_change, href_change_2).diff()[2]
        self.assertTrue(tag_change_class_insert in combined_diff)
        self.assertTrue(tag_change_class_delete in combined_diff)

    def test_command_line(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp1:
            tmp1.write(html_str.encode())

        with tempfile.NamedTemporaryFile(delete=False) as tmp2:
            tmp2.write(html_different_str.encode())

        result = subprocess.check_output(["python", "-m", "htmldiffer", tmp1.name, tmp2.name])
        diff_results = str(result.decode()).split('</html>')
        self.assertTrue(tag_change_class_delete in diff_results[0])
        self.assertTrue(tag_change_class_insert in diff_results[1])

def main():
    unittest.main()

if __name__ == '__main__':
    main()
