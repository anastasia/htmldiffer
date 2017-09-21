import os
import difflib
from .utils import html2list, add_style_str, is_tag
from .settings import STYLE_STR, EXCLUDE_STRINGS_A, EXCLUDE_STRINGS_B, WHITELISTED_TAGS, ADD_STYLE


class HTMLDiffer:
    def __init__(self, html_a, html_b):
        if os.path.isfile(html_a):
            with open(html_a, "r") as file_a:
                self.html_a = file_a.read()
        else:
            self.html_a = html_a
        if os.path.isfile(html_b):
            with open(html_b, "r") as file_b:
                self.html_b = file_b.read()
        else:
            self.html_b = html_b

        self.deleted_diff, self.inserted_diff, self.combined_diff = self.diff()

    def diff(self):
        """Takes in strings a and b and returns HTML diffs: deletes, inserts, and combined."""

        a, b = html2list(self.html_a), html2list(self.html_b)
        if ADD_STYLE:
            a, b = add_style_str(a, custom_style_str=STYLE_STR), add_style_str(b, custom_style_str=STYLE_STR)

        out = [[], [], []]

        try:
            # autojunk can cause malformed HTML, but also speeds up processing.
            s = difflib.SequenceMatcher(None, a, b, autojunk=False)
        except TypeError:
            s = difflib.SequenceMatcher(None, a, b)

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

        return ''.join(out[0]), ''.join(out[1]), ''.join(out[2])


def diff_tag(diff_type, text):
    return '<span class="diff_%s">%s</span>' % (diff_type, text)


def no_changes_exist(old_el, new_el):
    old_el_str = ''.join(old_el)
    new_el_str = ''.join(new_el)
    if len(EXCLUDE_STRINGS_A):
        for s in EXCLUDE_STRINGS_A:
            old_el_str = ''.join(old_el_str.split(s))
    if len(EXCLUDE_STRINGS_A):
        for s in EXCLUDE_STRINGS_B:
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
    idx, just_text, outcome = [0, '', []]
    joined = ''.join(text_list)

    if joined.isspace():
        return joined

    while idx < len(text_list):
        whitelisted = False
        el = text_list[idx]

        if is_tag(el) or el.isspace() or el == '':
            for tag in WHITELISTED_TAGS:
                if tag in el:
                    outcome.append(diff_tag(diff_type, el))
                    whitelisted = True
                    break
            if not whitelisted:
                outcome.append(el)
        else:
            outcome.append(diff_tag(diff_type, el))
        idx += 1

    return ''.join(outcome)
