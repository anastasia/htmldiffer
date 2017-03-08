#!/usr/bin/python
"""HTML Diff: http://www.aaronsw.com/2002/diff
Rough code, badly documented. Send me comments and patches."""

__author__ = 'Aaron Swartz <me@aaronsw.com>'
__copyright__ = '(C) 2003 Aaron Swartz. GNU GPL 2 or 3.'
__version__ = '0.22'

import difflib, string, re

def isTag(x):
    return x[0] == "<" and x[-1] == ">"

def textDiff(a, b):
    """Takes in strings a and b and returns a human-readable HTML diff."""

    out = []
    a, b = html2list(a), html2list(b)
    try: # autojunk can cause malformed HTML, but also speeds up processing.
        s = difflib.SequenceMatcher(None, a, b, autojunk=False)
    except TypeError:
        s = difflib.SequenceMatcher(None, a, b)
    for e in s.get_opcodes():
        if e[0] == "replace":
            # @@ need to do something more complicated here
            # call textDiff but not for html, but for some html... ugh
            # gonna cop-out for now
            """ ignoring all tags """
            idx = e[3]
            while idx <= e[4]:
                just_text = ''
                if not isTag(b[idx]):
                    just_text += b[idx]
                else:
                    if len(just_text):
                        out.append('<span class="diff_insert">'+''.join(just_text)+'</span>')
                        just_text = ''
                        out.append(''.join(b[idx]))
                if len(just_text):
                    out.append('<span class="diff_insert">'+''.join(just_text)+'</span>')
                idx += 1

        elif e[0] == "delete":
            out.append('<span class="diff_delete">'+ ''.join(a[e[1]:e[2]]) + "</span>")
        elif e[0] == "insert":
            out.append('<span class="diff_insert">'+''.join(b[e[3]:e[4]]) + "</span>")
        elif e[0] == "equal":
            out.append(''.join(b[e[3]:e[4]]))
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

def html2list(x, b=0):
    rx = re.compile('\n|\t|\r|\s{2}')
    mode = 'char'
    cur = ''
    out = []
    x = rx.sub('', x)

    for c in x:
        if mode == 'tag':
            if c == '>':
                if b: cur += ']'
                else: cur += c
                out.append(cur); cur = ''; mode = 'char'
            else: cur += c
        elif mode == 'char':
            if c == '<':
                out.append(cur)
                if b: cur = '['
                else: cur = c
                mode = 'tag'
            elif c in string.whitespace: out.append(cur+c); cur = ''
            else: cur += c
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
    print textDiff(open(a).read(), open(b).read())
