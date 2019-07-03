import re
import os

from bs4 import BeautifulSoup

from . import settings


def html2list(html_string, level='word'):
    """
    :param  html_string: any ol' html string you've got
            level:  either 'word' or 'character'. If level='word', elements will be words.
                    If level='character', elements will be individial characters.
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
    # different modes for parsing
    CHAR, TAG = 'char', 'tag'

    mode = CHAR
    cur = ''
    out = []

    # TODO: use generators
    # iterate through the string, character by character
    for c in html_string:

        # tags must be checked first to close tags
        if mode == TAG:

            # add character to current element
            cur += c

            # if we see the end of the tag
            if c == '>':
                out.append(cur)  # add the current element to the output
                cur = ''         # reset the character
                mode = CHAR      # set the mode back to character mode

        elif mode == CHAR:

            # when we are in CHAR mode and see an opening tag, we must switch
            if c == '<':

                # clear out string collected so far
                if cur != "":
                    out.append(cur)   # if we have already started a new element, store it
                cur = c               # being our tag
                mode = TAG            # swap to tag mode
            
            # if c is a special character, store 'word', store c, continue
            elif is_special_character(c):
                out.append(cur)
                out.append(c)
                cur = ''
            
            # otherwise, simply continue building up the current element
            else:
                if level == 'word':
                    cur += c
                elif level == 'character':
                    out.append(c)
                else:
                    raise ValueError('level must be "word" or "character"')

    # TODO: move this to its own function `merge_blacklisted` or `merge_tags` return to a generator instead of list
    cleaned = list()
    blacklisted_tag = None
    blacklisted_string = ""

    for x in out:
        if not blacklisted_tag:
            for tag in settings.BLACKLISTED_TAGS:
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


def check_html(html, encoding=None):
    if isinstance(html, BeautifulSoup):
        html = html.prettify()    
    elif os.path.isfile(html):
        with open(html, "r", encoding=encoding) as file:
            html = file.read()
    else:
        html = html
    return html


def verified_blacklisted_tag(x, tag):
    """
    check for '<' + blacklisted_tag +  ' ' or '>'
    as in: <head> or <head ...> (should not match <header if checking for <head)
    """
    initial = x[0:len(tag) + 1 + 1]
    blacklisted_head = "<{0}".format(tag)
    return initial == (blacklisted_head + " ") or initial == (blacklisted_head + ">")


def add_stylesheet(html_list):
    stylesheet_tag = '<link rel="stylesheet" type="text/css" href="{}">'.format(settings.STYLESHEET)
    for idx, el in enumerate(html_list):
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


def compare_tags(tag_a, tag_b):
    """
    returns markers for deleted, inserted, and combined
    """
    tag_parts_a = chart_tag(tag_a)
    tag_parts_b = chart_tag(tag_b)

    # first test whether we have any new attributes
    deleted_attributes = set(tag_parts_a.keys()) - set(tag_parts_b.keys())
    inserted_attributes = set(tag_parts_b.keys()) - set(tag_parts_a.keys())

    # then look at every attribute set and check whether the values are the same
    changed_attributes = list()
    for attribute in set(tag_parts_a.keys()) & set(tag_parts_b.keys()):
        if tag_parts_a[attribute] != tag_parts_b[attribute]:
            changed_attributes.append(attribute)

    return {
        'deleted_attributes': list(deleted_attributes),
        'inserted_attributes': list(inserted_attributes),
        'changed_attributes': changed_attributes,
    }


def chart_tag(tag_string):
    """
    Takes tag and returns dict that charts out tag parts
    example:
        tag = '<div title="somewhere">'
        parts = chart_tag(tag)
        print(parts)
        # {'tag': 'div', 'title': 'somewhere'}
    """
    tag_parts = dict()
    if tag_string[0] != "<" and tag_string[-1] != ">":
        raise Exception("Got malformed tag", tag_string)

    t = tag_string.split(" ")
    for el in t:
        if el[0] == "<":
            # grab the tag type
            tag_parts['tag'] = el[1:]
        else:
            check_element = el[:-1] if el[-1] == ">" else el
            check_element = check_element.replace('"', '').replace('/', '')

            if len(check_element.split("=")) > 1:
                attribute, values = check_element.split("=")
                tag_parts[attribute] = values
            else:
                # if unattached elements, these are probably extra values from
                # the previous attribute, so we add them
                tag_parts[attribute] += ' ' + check_element
            if el[-1] == ">":
                return tag_parts


def get_class_decorator(name, diff_type=''):
    """returns class like `htmldiffer-tag-change`"""
    if diff_type:
        return "%s_%s" % (settings.HTMLDIFFER_CLASS_STRINGS[name], diff_type)
    else:
        return "%s" % (settings.HTMLDIFFER_CLASS_STRINGS[name])


# ===============================
# Predicate functions
# ===============================
# Note: These make assumptions about consuming valid html text. Validations should happen before these internal
# predicate functions are used -- these are not currently used for parsing.

def is_blacklisted_tag(tag):
    return tag in settings.BLACKLISTED_TAGS


def is_comment(text):
    return "<!--" in text


def is_ignorable(text):
    return is_comment(text) or is_closing_tag(text) or text.isspace()


def is_whitelisted_tag(tag):
    # takes a tag and checks against WHITELISTED
    return tag in settings.WHITELISTED_TAGS


def is_open_script_tag(x):
    return "<script " in x


def is_closed_script_tag(x):
    return "<\script" in x


def is_tag(x):
    return len(x) > 0 and x[0] == "<" and x[-1] == ">"


def is_opening_tag(x):
    return x[0] == "<" and x[1] != "/"


def is_closing_tag(x):
    return x[0:2] == "</"


def is_self_closing_tag(x):
    return len(x) > 0 and x[0] == "<" and x[-2:] == "/>"


def is_text(x):
    return ("<" not in x) and (">" not in x)


def is_div(x):
    return x[0:4] == "<div" and x[-6:] == "</div>"


def is_special_character(string):
    char_re = re.compile(r'[^a-zA-Z0-9]')
    string = char_re.search(string)
    return bool(string)
