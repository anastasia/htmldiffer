from htmldiff import settings

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

    cleaned = list()
    blacklisted_tag = None
    blacklisted_string = ""

    for x in out:
        if not blacklisted_tag:
            for tag in settings.BLACKLISTED_TAGS:
                if x[0:len(tag)+1] == "<{0}".format(tag):
                    blacklisted_tag = tag
                    blacklisted_string += x
                    break
            else:
                cleaned.append(x)
        else:
            # print "else", x, "</%s>" % blacklisted_tag
            if x == "</{0}>".format(blacklisted_tag):
                blacklisted_string += x
                cleaned.append(blacklisted_string)
                blacklisted_tag = None
                blacklisted_string = ""
            else:
                blacklisted_string += x
                # print blacklisted_string

    return cleaned

def add_style_str(html_list):
    style_str = settings.CUSTOM_STYLE_STR if settings.CUSTOM_STYLE_STR else settings.STYLE_STR

    for idx,el in enumerate(html_list):
        if "</head>" in el:
            head = el.split("</head>")
            new_head = head[0] + style_str + "</head>" + "".join(head[1:])
            html_list[idx] = new_head

    return html_list

def is_comment(text):
    if "<!--" in text:
        return True
    return False

def is_closing_tag(text):
    if '</' in text:
        return True
    return False

def is_ignorable(text):
    if is_comment(text) or is_closing_tag(text) or text.isspace():
        return True
    return False

def is_whitelisted_tag(x):
    for tag in settings.WHITELISTED_TAGS:
        if "<%s" % tag in x:
            return True
    return False

def is_open_script_tag(x):
    if "<script " in x:
        return True
    return False

def is_closed_script_tag(x):
    if "<\script " in x:
        return True
    return False

def is_tag(x):
    if not len(x):
        return False
    return x[0] == "<" and x[-1] == ">"

def is_text(x):
    return ("<" and ">") not in x

def is_div(x):
    return x[0:4] == "<div" and x[-6:] == "</div>"
