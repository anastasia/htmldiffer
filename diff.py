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
    """Takes in strings a and b and returns a human-readable HTML diff."""

    out = []
    a, b = html2list(a), html2list(b)
    try: # autojunk can cause malformed HTML, but also speeds up processing.
        s = difflib.SequenceMatcher(None, a, b, autojunk=False)
    except TypeError:
        s = difflib.SequenceMatcher(None, a, b)
    for e in s.get_opcodes():
        import ipdb; ipdb.set_trace()
        old_el = a[e[1]:e[2]]
        new_el = b[e[3]:e[4]]
        if e[0] == "replace" or e[0] == "insert":
            out.append(wrap_text("insert", new_el))
        elif e[0] == "delete":
            out.append(wrap_text("delete", old_el))
        elif e[0] == "equal":
            out.append(''.join(new_el))
        else:
            raise "Um, something's broken. I didn't expect a '" + `e[0]` + "'."
    out.append("""<style>
        span.diff_insert {
            background-color: #a0ffa0 !important;
            z-index: 100000;
        }
        span.diff_delete {
            background-color: red !important;
            z-index: 100000;
        }
    </style>""")
    return ''.join(out)

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



def html2list(x, b=0):
    rx = re.compile('\n|\t|\r|\s{2}')
    mode = 'char'
    cur = ''
    out = []
    x = rx.sub('', x)

    for c in x:
        if mode == 'tag':
            if c == '>':
                if b:
                    cur += ']'
                else:
                    cur += c
                out.append(cur); cur = ''; mode = 'char'
            else:
                cur += c
        elif mode == 'char':
            if c == '<':
                out.append(cur)
                if b:
                    cur = '['
                else:
                    cur = c
                mode = 'tag'
            elif c in string.whitespace:
                out.append(cur+c); cur = ''
            else:
                cur += c
    out.append(cur)
    return filter(lambda x: x is not '', out)

if __name__ == '__main__':
    import sys
    try:
        a, b = sys.argv[1:3]
    except ValueError:
        print "htmldiff: highlight the differences between two html files"
        print "usage: " + sys.argv[0] + " a b"
        sys.exit(1)
    print text_diff(open(a).read(), open(b).read())
