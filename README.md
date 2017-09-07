###Diffing HTML
[![Build Status](https://travis-ci.org/anastasia/htmldiff.svg?branch=develop)](https://travis-ci.org/anastasia/htmldiff)
#

htmldiff works by using difflib's [SequenceMatch](https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher) algorithm. 

+ htmldiff's text_diff method (in [diff.py](https://github.com/anastasia/htmldiff/blob/develop/htmldiff/diff.py)) iterates through all of the change sets created by the SequenceMatch (the sets are now a series of elements).
+ For each element, if the element is not an html tag, it wraps it in a `<span>` tag with a `diff_insert` or `diff_delete` class.
+ If the element is an HTML tag, text_diff will skip the element *unless* the element is in `settings.WHITELISTED_TAGS` list.
  + HTML `<!-- comments -->` will be read as tags and therefore skipped. 
  + all text that is changed (as opposed to the tags that surround it) should therefore be wrapped by appropriate `span` diff tags.
  + the default whitelisted tags include self-closing tags `<img>` and `<input>` 
  

