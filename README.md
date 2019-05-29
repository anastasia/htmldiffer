## htmldiffer
[![Build Status](https://travis-ci.org/anastasia/htmldiffer.svg?branch=develop)](https://travis-ci.org/anastasia/htmldiff)
#### highlight the differences between two html files
#
### To install:
```
pip install htmldiffer
```

Or
```
$ git clone git@github.com:anastasia/htmldiffer.git
$ cd htmldiffer
$ python -m htmldiffer file_one.html file_two.html
```

HTMLDiffer will take strings or files and return three html diffs: deleted diff, inserted diff, and a combined diff (showing both the deleted and inserted highlights). To use this in a library:
HTMLDiffer will 
+ surround any text-level changes with `<span class="htmldiffer_[insert|delete]>`
+ insert htmldiffer classes (`class="htmldiffer-tag-change_[insert|delete]`) into any tag-level changes (that is, if a tagname has changed, or any attribute inside a tag has changed) 

```python
from htmldiffer import diff

str_a = "<html><body>Hello world!</body></html>"
str_b = "<html><body>Hello wanda! Hello!</body></html>"
d = diff.HTMLDiffer(str_a, str_b)

print(d.deleted_diff)
# get a string of the HTML with deleted elements highlighted:
# <html><body>Hello <span class="diff_delete">world!</span></body></html>

print(d.inserted_diff)
# get a string of the HTML with inserted elements highlighted:
# <html><body>Hello <span class="diff_insert">wanda! </span><span class="diff_insert">Hello!</span></body></html>

print(d.combined_diff)
# get a string of the HTML with both deleted and inserted elements highlighted:
# <html><body>Hello <span class="diff_delete">world!</span><span class="diff_insert">wanda! </span><span class="diff_insert">Hello!</span></body></html>
```

That's it!

### How does this work?

htmldiffer takes a string or a file of html, converts it to string entities[1], then diffs those entities using [SequenceMatcher][seqmatch] 
and gets deleted, inserted, and combined (deleted and inserted) html, which include spans wrapping the changed text.

Example:
```python

old_html = "<h1>This is a simple header</h1>"
new_html = "<h1>This is a newer, better header</h1>"

d = HTMLDiffer(old_html, new_html)
d.deleted_diff == "<h1>This is a <span class="diff_delete">simple </span>header</h1>"
d.inserted_diff == "<h1>This is a <span class="diff_insert">newer, </span><span class="diff_insert">better </span>header</h1>"
d.combined_diff == "<h1>This is a <span class="diff_delete">simple </span><span class="diff_insert">newer, </span><span class="diff_insert">better </span>header</h1>"
```

[1] An entity can be one of several things:
+ A word
+ An opening tag: `<li class="list-element" style="some:style;">`
+ A closing tag: `</li>`
+ A tag that has been whitelisted (self closing tags that you want to highlight changes of are recommended here)
    + for instance, by default we're whitelisting image tags, so the entity will be: `<img src="some/source.jpg"/>`
+ The entirety of a blacklisted tag (like a script and head tag, since it's difficult to show changes in those, for now)
    + `<script>The entirety of a script tag will be a single entity</script>`

In order to maintain the integrity and structure of the original HTML, we don't remove any whitespaces or change the HTML itself in any way, before iterating through and wrapping it with span tags.

[seqmatch]:https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher


### Tell me more

+ htmldiffer's `diff` method [diff.py][diffpy]
`tokenize_html` method which iterates through the html string and spits out a list of entities (see above for explanation).

[diffpy]:https://github.com/anastasia/htmldiffer/htmldiffer/diff.py

+ `diff` adds a style string (default lives in settings.py) to the `<head>` of the html (if head tag exists)
  so that our diff highlights show up

+ `diff` compares the two newly created lists (two — one is for the old html string, one for the new html string) using
  `SequenceMatcher`, and gets a list back describing (using codes 'replace', 'delete', 'insert', and 'equal'), for each
   element A how it got to be element B

+ `diff` method iterates through that list, calling to `wrap_text` to wrap each element according to its change value

More complexities! How does `wrap_text` work?

+ For each element, if the element is not an html tag, it wraps it in a `<span>` tag with a `diff_insert` or `diff_delete` class.

+ If the element is an HTML tag, `wrap_text` will skip the element *unless* the element is in `settings.WHITELISTED_TAGS` list.
  The reason for that is that we don't want to wrap the `<li>` opening tag itself, but the changes within that tag.


  Things to note:

  + HTML `<!-- comments -->` will be read as a tag and therefore skipped. 
  + all text that is changed should therefore be wrapped by appropriate `span` diff tags.
  + the default whitelisted tags include self-closing tags `<img>` and `<input>` and will therefore be wrapped in `span` diff tags 


***

This repository is a fork off of https://github.com/aaronsw/htmldiff. 
