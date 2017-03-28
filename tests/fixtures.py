html_str = """
<html>
    <head class="this_is_a_class">
        <script src="some_js.js"></script>
    </head>
    <body>
      <div>
         test <b> test</b> foo
      </div>
      <div>
         del
      </div>
    </body>
</html>
"""

html_different_str = """
<html>
    <head class="this_is_a_class">
        <script src="some_js.js"></script>
    </head>
    <body>
      <div class="new_class"><p>New div!</p></div>
      <div>
         TEst <b> toost</b> toast
      </div>
    </body>
</html>
"""

img_tag = '<img src="smiley.gif" alt="Smiley face" height="42" width="42">'
div_tag = '<div id="best_container" class="container">img</div>'
