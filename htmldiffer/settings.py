# use yaml and look in "~/.config/htmldiffer/settings.yaml" or make it? also where you can put "~/.config/htmldiffer/styles.css"
IGNORE_HEAD_CHANGES = True
ADD_STYLE = True
CUSTOM_STYLE_STR = ""
WHITELISTED_TAGS = ["img", "input"]
BLACKLISTED_TAGS = ["head", "script", "style", "noscript"]

EXCLUDE_STRINGS_A = []
EXCLUDE_STRINGS_B = []

TAG_CHANGE_PREFIX = "diff_tag_"
TEXT_CHANGE_PREFIX = "diff_"

STYLESHEET = "../assets/htmldiffer_stylesheet.css"

STRING_PREFIX = "htmldiffer"

HTMLDIFFER_CLASS_STRINGS = {
    'change': "%s" % STRING_PREFIX,
    'tag_change': "%s-tag-change" % STRING_PREFIX,
    'attribute_change': "%s-attribute-change" % STRING_PREFIX,
    'class_change': "%s-class-change" % STRING_PREFIX,
    'id_change': "%s-id-change" % STRING_PREFIX,
    'text_insert': "%s-insert" % STRING_PREFIX,
    'text_delete': "%s-delete" % STRING_PREFIX,
}
