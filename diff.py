#!/usr/bin/python
"""HTML Diff: http://www.aaronsw.com/2002/diff
Rough code, badly documented. Send me comments and patches."""

__author__ = 'Aaron Swartz <me@aaronsw.com>'
__copyright__ = '(C) 2003 Aaron Swartz. GNU GPL 2 or 3.'
__version__ = '0.22'

import difflib, string, re

def diff_tag(diff_type, text):
    if is_tag(text):
        # print "is tag:", text
        return "<span class=diff_%s>%s</span>" % (diff_type, text)
    else:
        return "<span class=diff_%s>%s</span>" % (diff_type, text)

def is_tag(x):
    return x[0] == "<" and x[-1] == ">"

def is_text(x):
    return ("<" and ">") not in x

def is_div(x):
    return x[0:4] == "<div" and x[-6:] == "</div>"

def text_diff(a, b):
    """Takes in strings a and b and returns HTML diffs: deletes, inserts, and combined."""

    out = [[], [], []]
    a, b = convert_to_clean_list(a), convert_to_clean_list(b)
    try: # autojunk can cause malformed HTML, but also speeds up processing.
        s = difflib.SequenceMatcher(None, a, b, autojunk=False)
    except TypeError:
        s = difflib.SequenceMatcher(None, a, b)
    for e in s.get_opcodes():
        old_el = a[e[1]:e[2]]
        new_el = b[e[3]:e[4]]
        if e[0] == "replace":
            deletion = wrap_text("delete", old_el)
            insertion = wrap_text("insert", new_el)
            out[0].append(deletion)
            out[1].append(insertion)
            out[2].append(deletion + insertion)
        elif e[0] == "delete":
            out[0].append(wrap_text("delete", old_el))
            out[2].append(wrap_text("delete", old_el))
        elif e[0] == "insert":
            out[1].append(wrap_text("insert", new_el))
            out[2].append(wrap_text("insert", new_el))
        elif e[0] == "equal":
            out[0].append(''.join(new_el))
            out[1].append(''.join(new_el))
            out[2].append(''.join(new_el))
        else:
            raise "Um, something's broken. I didn't expect a '" + `e[0]` + "'."
    return (''.join(out[0]), ''.join(out[1]), ''.join(out[2]))

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
    rx = re.compile('\n|\t|\r')
    html_string = rx.sub('', html_string)
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


    out_without_spaces = filter(lambda el: el is not '' and el is not ' ', out)
    out_with_the_head = []

    # treat <head>:</head> as one string (everything up to head tag close)
    # so that it's easier to insert style
    for idx, x in enumerate(out_without_spaces):
        if "</head>" in x:
            break

    head = "".join(out_without_spaces[0:idx])
    out_with_the_head.append(head)
    for idx2, x2 in enumerate(out_without_spaces[idx:]):
        out_with_the_head.append(x2)

    return out_with_the_head

def convert_to_clean_list(html_string):
    a = html2list(html_string)
    return add_style_collapse_head(a)

def add_style_collapse_head(html_list):
    new_html_list = []
    style_string_hack = "<style>span.diff_insert {background-color: #a0ffa0 !important; z-index: 100000;} span.diff_delete {background-color: #ffecec !important; z-index: 100000; }</style>"
    for idx, x in enumerate(html_list):
        if "</head>" in x:
            break
    x_parts = x.split("</head>")
    new_head_string = "".join(html_list[0:idx-1]) + x_parts[0] + style_string_hack + x_parts[1]
    new_html_list.append(new_head_string)

    for y in html_list[idx+1:]:
        new_html_list.append(y)

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
