from .settings import *
from .rules import *


def tokenize_html(html_string):
    """
    takes any ol' html string you've got
    and returns a generator of elements, making sure not to break up open tags (even if they contain attributes)

    Example:
        html_str = "<h1>This is a simple header</h1>"
        result = tokenize_html(html_str)
        list(result)
        ['<h1>', 'This ', 'is ', 'a ', 'simple ', 'header', '</h1>']

    if html_str includes any BLACKLISTED tags, tokenize_html keeps those tags closed

    Example:
        BLACKLISTED_TAGS = ['head']
        html_str = "<head><title>Page Title</title></head>"
        result = list(tokenize_html(html_str))
        result
        # ['<head><title>Page Title</title></head>']
    """
    # different modes for parsing
    CHAR, TAG, BLACKLISTED = 'char', 'tag', 'blacklisted'

    mode = CHAR
    current_el = ''
    blacklisted_tag = None

    # iterate through the string, character by character
    for char in html_string:
        # tags must be checked first to close tags
        if mode == TAG:
            # add character to current element
            current_el += char

            # if we see the end of the tag
            if char == '>':
                # check element is blacklisted tag
                try:
                    tagname = extract_tagname(current_el)
                    if is_blacklisted_tag(tagname):
                        mode = BLACKLISTED
                        blacklisted_tag = tagname
                    else:
                        mode = CHAR
                        yield current_el
                        current_el = ''

                except ValueError as e:
                    yield current_el
                    current_el = ''         # reset the character
                    mode = CHAR      # set the mode back to character mode

        elif mode == CHAR:
            # when we are in CHAR mode and see an opening tag
            # switch to TAG mode
            if char == '<':
                if current_el != "":
                    yield current_el # clear out string collected so far

                current_el = char
                mode = TAG        # swap to tag mode

            # when we reach the next 'word', store and continue
            elif char.isspace():
                current_el += char
                # out.append(cur+c)   # NOTE: we add spaces here so that we preserve structure
                yield current_el
                current_el = ''

            # otherwise, simply continue building up the current element
            else:
                current_el += char
        elif mode == BLACKLISTED:
            # check if closing blacklisted tag
            current_el += char
            if is_complete_tag_block(blacklisted_tag, current_el):
                # we're done with the blacklisted tag
                # yield current_el and return everything to normal
                yield current_el
                current_el = ''
                mode = CHAR
                blacklisted_tag = None


def is_complete_tag_block(tag, html_str):
    """
    takes a tag and an html_str and returns whether or not the
    string contains in it the complete closed tag
    """
    # remove all the spaces because valid HTML can have extra spaces inside
    # opening and closing tags, like <input />
    spaceless_html_str = html_str.replace(" ", "")
    start_tag_is_present = spaceless_html_str[:len(tag)+1] == "<%s" % tag
    if tag in self_closing_tags:
        return start_tag_is_present and html_str[-1] == ">"
    else:
        end_tag_is_present = spaceless_html_str[-1 * (len(tag) + 3):] == "</%s>" % tag
        return start_tag_is_present and end_tag_is_present


def add_stylesheet(html_list):
    stylesheet_tag = '<link rel="stylesheet" type="text/css" href="{}">'.format(STYLESHEET)
    for idx, el in enumerate(html_list):
        if "</head>" in el:
            # add at the very end of head tag cause we is important
            head = el.split("</head>")
            new_head = head[0] + stylesheet_tag + "</head>" + "".join(head[1:])
            html_list[idx] = new_head

    return html_list


def extract_tagname(el):
    if not is_tag(el):
        raise ValueError("Not a tag!")

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
        return "%s_%s" % (HTMLDIFFER_CLASS_STRINGS[name], diff_type)
    else:
        return "%s" % (HTMLDIFFER_CLASS_STRINGS[name])


# ===============================
# Predicate functions
# ===============================
# Note: These make assumptions about consuming valid html text. Validations should happen before these internal
# predicate functions are used -- these are not currently used for parsing.


def is_blacklisted_tag(tag):
    return tag in BLACKLISTED_TAGS


def is_comment(text):
    return "<!--" in text


def is_ignorable(text):
    return is_comment(text) or is_closing_tag(text) or text.isspace()


def is_whitelisted_tag(tag):
    # takes a tag and checks against WHITELISTED
    return tag in WHITELISTED_TAGS


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
    tag = extract_tagname(x)
    return tag in self_closing_tags


def is_text(x):
    return ("<" not in x) and (">" not in x)


def is_div(x):
    return x[0:4] == "<div" and x[-6:] == "</div>"
