#### Diffing HTML
[![Build Status](https://travis-ci.org/anastasia/htmldiff.svg?branch=develop)](https://travis-ci.org/anastasia/htmldiff)
#

htmldiff works by using difflib's [SequenceMatch](https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher) algorithm. 
The logic is a little bit complex! So let's dive in:

+ htmldiff's `text_diff` method ([diff.py](https://github.com/anastasia/htmldiff/blob/develop/htmldiff/diff.py)) calls to htmldiff's [utils.py](https://github.com/anastasia/htmldiff/blob/develop/htmldiff/utils.py)  `html2list` method which iterates through the html string and spits out a list of entities.
  + All opening tags will be kept together as an entity 
      - example: `<li class="list-element" style="some:style;">`
  + Words remain unbroken
  + All blacklisted tags will remain unbroken (for instance, since there is no way to see changes in the `<head>` tag right now, we keep the tag and all of its contents as one element)

+ `text_diff` calls to utils to add a style string (default lives in settings.py) to the `<head>` of the html (if head tag exists) so that our diff highlights show up
+ `text_diff` compares the two newly created lists (two, because one is for the old html string and the other is for the new html string) using SequenceMatch, and gets
    a list back describing how A element got to be B element
+ `text_diff` method iterates through that list, calling to `wrap_text` to wrap each element according to its change value

More complexities! How does `wrap_text` work?
+ For each element, if the element is not an html tag, it wraps it in a `<span>` tag with a `diff_insert` or `diff_delete` class.
+ If the element is an HTML tag, `wrap_text` will skip the element *unless* the element is in `settings.WHITELISTED_TAGS` list.
  + HTML `<!-- comments -->` will be read as tags and therefore skipped. 
  + all text that is changed (as opposed to the tags that surround it) should therefore be wrapped by appropriate `span` diff tags.
  + the default whitelisted tags include self-closing tags `<img>` and `<input>` 
 

To install:
```
$ git clone git@github.com:anastasia/htmldiff.git
$ cd htmldiff
```
If you want to work in python, open a python shell script:
```
ipython
```
Get three html diffs: deleted diff, inserted diff, and a combined diff (of deleted and inserted — this could be confusing to view)
```python
from htmldiff import diff

deletes_diff, inserts_diff, combined_diff = diff.text_diff(html_string_one, html_string_two)
```

To do the above in terminal, instead:
```
$ python diff.py file_one.html file_two.html
```
