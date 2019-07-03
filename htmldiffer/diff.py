from bs4 import BeautifulSoup
import difflib
from . import settings
from . import utils


class HTMLDiffer:
    def __init__(self, html_a, html_b, diff_level='word', encoding=None, autojunk=False):
        html_a = utils.check_html(html_a, encoding=encoding), 
        html_b = utils.check_html(html_b, encoding=encoding)

        diff = self.diff(html_a, html_b,
                         diff_level=diff_level, 
                         autojunk=autojunk)
        self.deleted_diff, self.inserted_diff, self.combined_diff = diff[0:3]
        self.s = diff[3]
        
    def diff(self, html_a, html_b, diff_level='word', autojunk=False):
        """Takes in strings a and b and returns HTML diffs: deletes, inserts, and combined."""

        a, b = utils.html2list(html_a, level=diff_level), utils.html2list(html_b, level=diff_level)
        if settings.ADD_STYLE:
            a, b = utils.add_stylesheet(a), utils.add_stylesheet(b)
        try:
            # autojunk can cause malformed HTML, but also speeds up processing.
            s = difflib.SequenceMatcher(None, a, b, autojunk=autojunk)
        except TypeError:
            s = difflib.SequenceMatcher(None, a, b)
        
        deleted_diff, inserted_diff, combined_diff = diff_from_sequence_matcher(s, a, b)
        
        return deleted_diff, inserted_diff, combined_diff, s
    
    def ratio(self):
        return self.s.ratio()


def diff_from_sequence_matcher(s, a, b):
    out = [[], [], []]
    for e in s.get_opcodes():
        old_el = a[e[1]:e[2]]
        new_el = b[e[3]:e[4]]

        if e[0] == "equal" or no_changes_exist(old_el, new_el):
            append_text(out, deleted=''.join(old_el), inserted=''.join(new_el), both=''.join(new_el))

        elif e[0] == "replace":
            deletion = wrap_text("delete", old_el)
            insertion = wrap_text("insert", new_el)
            append_text(out, deleted=deletion, inserted=insertion, both=deletion + insertion)

        elif e[0] == "delete":
            deletion = wrap_text("delete", old_el)
            append_text(out, deleted=deletion, inserted=None, both=deletion)

        elif e[0] == "insert":
            insertion = wrap_text("insert", new_el)
            append_text(out, deleted=None, inserted=insertion, both=insertion)

        else:
            raise "Um, something's broken. I didn't expect a '" + repr(e[0]) + "'."

    deleted_diff = ''.join(out[0])
    inserted_diff = ''.join(out[1])

    # using BeautifulSoup to fix any potentially broken tags
    # see https://github.com/anastasia/htmldiffer/issues/28
    combined_diff = str(BeautifulSoup(''.join(out[2]), 'html.parser'))
    return deleted_diff, inserted_diff, combined_diff
    

def add_diff_tag(diff_type, text):
    diff_class = utils.get_class_decorator("change", diff_type)
    return '<span class="%s">%s</span>' % (diff_class, text)


def add_diff_class(diff_type, original_tag):
    # if closing tag like </div> return out immediately
    if utils.is_closing_tag(original_tag):
        return original_tag

    diff_class = utils.get_class_decorator("tag_change", diff_type)

    if len(original_tag.split("class=")) > 1:
        # determine if single or double quote
        tag_parts = original_tag.split("class=")
        if tag_parts[1][0] == '"':
            contents = tag_parts[1].split('"')
        else:
            # assuming presence of quotes, for now
            contents = tag_parts[1].split("'")
        beginning_of_content = tag_parts[0]
        class_content = contents[1]
        end_of_content = ''.join(contents[2:])
        new_tag = beginning_of_content + ' class="' + class_content + ' ' + diff_class + '"' + end_of_content
    else:
        if utils.is_self_closing_tag(original_tag):
            new_tag = original_tag[:-2] + ' class="%s"' % diff_class + "/>"
        else:
            new_tag = original_tag[:-1] + ' class="%s"' % diff_class + ">"
    return new_tag


def no_changes_exist(old_el, new_el):
    old_el_str = ''.join(old_el)
    new_el_str = ''.join(new_el)
    if len(settings.EXCLUDE_STRINGS_A):
        for s in settings.EXCLUDE_STRINGS_A:
            old_el_str = ''.join(old_el_str.split(s))
    if len(settings.EXCLUDE_STRINGS_A):
        for s in settings.EXCLUDE_STRINGS_B:
            new_el_str = ''.join(new_el_str.split(s))

    return old_el_str == new_el_str


def append_text(out, deleted=None, inserted=None, both=None):
    if deleted:
        out[0].append(deleted)
    if inserted:
        out[1].append(inserted)
    if both:
        out[2].append(both)


def wrap_text(diff_type, text_list):
    idx, outcome = 0, []
    joined = ''.join(text_list)

    if joined.isspace():
        return joined

    while idx < len(text_list):
        el = text_list[idx]

        if utils.is_tag(el):
            tag = utils.extract_tagname(el)
            if utils.is_whitelisted_tag(tag):
                outcome.append(add_diff_tag(diff_type, el))
            else:
                # insert diff class into tag
                if utils.is_blacklisted_tag(tag):
                    outcome.append(el)
                else:
                    outcome.append(add_diff_class(diff_type, el))
        elif el.isspace() or el == '':
            # don't mark as changed
            outcome.append(el)
        else:
            outcome.append(add_diff_tag(diff_type, el))
        idx += 1

    return ''.join(outcome)

