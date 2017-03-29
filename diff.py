#!/usr/bin/python
"""HTML Diff: http://www.aaronsw.com/2002/diff
Rough code, badly documented. Send me comments and patches."""

__author__ = 'Aaron Swartz <me@aaronsw.com>'
__copyright__ = '(C) 2003 Aaron Swartz. GNU GPL 2 or 3.'
__version__ = '0.22'

import difflib, string, re

def diff_tag(diff_type, text):
    return '<span class="diff_%s">%s</span>' % (diff_type, text)
    # if is_tag(text):
    # else:
    #     return '<span class="diff_%s">%s</span>' % (diff_type, text)

def is_tag(x):
    if not len(x):
        return False
    return x[0] == "<" and x[-1] == ">"

def is_text(x):
    return ("<" and ">") not in x

def is_div(x):
    return x[0:4] == "<div" and x[-6:] == "</div>"

def text_diff(a, b):
    """Takes in strings a and b and returns HTML diffs: deletes, inserts, and combined."""

    a, b = html2list(a), html2list(b)
    a, b = add_style_str(a), add_style_str(b)

    out = [[], [], []]
    try:
        # autojunk can cause malformed HTML, but also speeds up processing.
        s = difflib.SequenceMatcher(None, a, b, autojunk=False)
    except TypeError:
        s = difflib.SequenceMatcher(None, a, b)

    for e in s.get_opcodes():
        old_el = a[e[1]:e[2]]
        new_el = b[e[3]:e[4]]
        if e[0] == "replace":
            deletion = wrap_text("delete", old_el)
            insertion = wrap_text("insert", new_el)
            append_text(out, deleted=deletion, inserted=insertion, both=deletion+insertion)
        elif e[0] == "delete":
            deletion = wrap_text("delete", old_el)
            append_text(out, deleted=deletion, inserted=None, both=deleted)
        elif e[0] == "insert":
            insertion = wrap_text("insert", new_el)
            append_text(out, deleted=None, inserted=insertion, both=insertion)
        elif e[0] == "equal":
            no_change = ''.join(new_el)
            append_text(out, deleted=no_change, inserted=no_change, both=no_change)
        else:
            raise "Um, something's broken. I didn't expect a '" + `e[0]` + "'."

    return (''.join(out[0]), ''.join(out[1]), ''.join(out[2]))

def append_text(out, deleted=None, inserted=None, both=None):
    if deleted:
        out[0].append(deleted)
    if inserted:
        out[1].append(inserted)
    if both:
        out[2].append(both)

def is_whitelisted_tag(x):
    whitelisted_tags = ["<img", "<input"]
    for tag in whitelisted_tags:
        if tag in x:
            return True
    return False

def wrap_text(diff_type, text_list):
    idx, just_text, outcome = [0, '', []]
    while idx < len(text_list):
        el = text_list[idx]
        if is_tag(el):
            if len(just_text):
                outcome.append(diff_tag(diff_type, just_text))
                just_text = ''
            if is_whitelisted_tag(el):
                outcome.append(diff_tag(diff_type, just_text))
            else:
                outcome.append(el)
        else:
            just_text += el
        idx += 1
    return ''.join(outcome)

def html2list(html_string, b=0):
    # rx = re.compile('\n|\t|\r')
    # html_string = rx.sub('', html_string)
    mode = 'char'
    cur = ''
    out = []

    for c in html_string:
        if mode == 'tag':
            cur += c
            if c == '>':
                out.append(cur)
                cur = ''
                mode = 'char'
        elif mode == 'char':
            if c == '<':
                # clear out string collected so far
                out.append(cur)
                cur = c
                mode = 'tag'
            elif c == ' ':
                out.append(cur+c)
                cur = ''
            else:
                cur += c


    # out_without_spaces = filter(lambda el: el is not '' and el is not ' ', out)
    out_with_the_head = []

    # treat <head>:</head> as one string (everything up to head tag close)
    # so that it's easier to insert style. also checking head for changes is not necessary

    for idx, x in enumerate(out):
        if "</head>" in x:
            break

    head = "".join(out[0:idx])
    out_with_the_head.append(head)
    for idx2, x2 in enumerate(out[idx:]):
        out_with_the_head.append(x2)

    return out_with_the_head

def add_style_str(html_list, style_str=None):
    if not style_str:
        style_str = "<style>span.diff_insert {background-color: #a0ffa0;} span.diff_delete {text-decoration: line-through;}</style>"
    new_html_list = [html_list[0] + style_str + html_list[1]] + html_list[2:]
    return new_html_list

if __name__ == '__main__':
    import sys
    try:
        a, b = sys.argv[1:3]
    except ValueError:
        print "htmldiff: highlight the differences between two html files"
        print "usage: " + sys.argv[0] + " a b"
        sys.exit(1)
    print text_diff(open(a).read(), open(b).read())
