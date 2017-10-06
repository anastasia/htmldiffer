from .settings import *


def html2list(html_string):
    """
    :param html_string: any ol' html string you've got
    :return: list of elements, making sure not to break up open tags (even if they contain attributes)
    Note that any blacklisted tag will not be broken up
    Example:
        html_str = "<h1>This is a simple header</h1>"
        result = html2list(html_str)
        result == ['<h1>', 'This ', 'is ', 'a ', 'simple ', 'header', '</h1>']

    Blacklisted tag example:
        BLACKLISTED_TAGS = ['head']
        html_str = "<head><title>Page Title</title></head>"
        result = html2list(html_str)
        result == ['<head><title>Page Title</title></head>']
    """
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
                if cur != "":
                    out.append(cur)
                cur = c
                mode = 'tag'
            elif c == ' ':
                out.append(cur+c)
                cur = ''
            else:
                cur += c

    cleaned = list()
    blacklisted_tag = None
    blacklisted_string = ""

    for x in out:
        if not blacklisted_tag:
            for tag in BLACKLISTED_TAGS:
                if verified_blacklisted_tag(x, tag):
                    blacklisted_tag = tag
                    blacklisted_string += x
                    break
            if not blacklisted_tag:
                cleaned.append(x)
        else:
            if x == "</{0}>".format(blacklisted_tag):
                blacklisted_string += x
                cleaned.append(blacklisted_string)
                blacklisted_tag = None
                blacklisted_string = ""
            else:
                blacklisted_string += x

    return cleaned


def verified_blacklisted_tag(x, tag):
    """
    check for '<' + blacklisted_tag +  ' ' or '>'
    as in: <head> or <head ...> (should not match <header if checking for <head)
    """
    initial = x[0:len(tag) + 1 + 1]
    blacklisted_head = "<{0}".format(tag)
    return initial == (blacklisted_head + " ") or initial == (blacklisted_head + ">")


def add_stylesheet(html_list):
    stylesheet_tag = '<link rel="stylesheet" type="text/css" href="{}">'.format(STYLESHEET)
    for idx,el in enumerate(html_list):
        if "</head>" in el:
            # add at the very end of head tag cause we is important
            head = el.split("</head>")
            new_head = head[0] + stylesheet_tag + "</head>" + "".join(head[1:])
            html_list[idx] = new_head

    return html_list


def extract_tagname(el):
    if not is_tag(el):
        raise Exception("Not a tag!")

    tag_parts = el[el.index('<')+1:el.index('>')].replace("/", "")
    return tag_parts.split(" ")[0]


def is_blacklisted_tag(el):
    tag = extract_tagname(el)
    return tag in BLACKLISTED_TAGS



def get_class_decorator(name, diff_type=''):
    """returns class like `htmldiffer-tag-change`"""
    if diff_type:
        return "%s_%s" % (HTMLDIFFER_CLASS_STRINGS[name], diff_type)
    else:
        return "%s" % (HTMLDIFFER_CLASS_STRINGS[name])


def is_comment(text):
    if "<!--" in text:
        return True
    return False


def is_ignorable(text):
    if is_comment(text) or is_closing_tag(text) or text.isspace():
        return True
    return False


def is_whitelisted_tag(x):
    for tag in WHITELISTED_TAGS:
        if "<%s" % tag in x:
            return True
    return False


def is_open_script_tag(x):
    if "<script " in x:
        return True
    return False


def is_closed_script_tag(x):
    if "</script " in x:
        return True
    return False


def is_tag(x):
    if not len(x):
        return False
    return x[0] == "<" and x[-1] == ">"


def is_opening_tag(x):
    return x[0] == "<" and x[1] != "/"


def is_closing_tag(x):
    return x[0:2] == "</"


def is_self_closing_tag(x):
    if not len(x):
        return False
    return x[0] == "<" and x[-2:] == "/>"


def is_text(x):
    return ("<" and ">") not in x


def is_div(x):
    return x[0:4] == "<div" and x[-6:] == "</div>"
