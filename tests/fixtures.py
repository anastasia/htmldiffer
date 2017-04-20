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
         not
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
span_tag = '<span id="spanning_not_spamming">it ain\'t a div or an img!</span>'

html_example_str = """<html><head>\n    <title>Example Domain</title>\n\n    <meta charset="utf-8">\n    <meta http-equiv="Content-type" content="text/html; charset=utf-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1">\n    <style type="text/css">\n    body {\n        background-color: #f0f0f2;\n        margin: 0;\n        padding: 0;\n        font-family: "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;\n\n    }\n    div {\n        width: 600px;\n        margin: 5em auto;\n        padding: 50px;\n        background-color: #fff;\n        border-radius: 1em;\n    }\n    a:link, a:visited {\n        color: #38488f;\n        text-decoration: none;\n    }\n    @media (max-width: 700px) {\n        body {\n            background-color: #fff;\n        }\n        div {\n            width: auto;\n            margin: 0 auto;\n            border-radius: 0;\n            padding: 1em;\n        }\n    }\n    </style>\n</head>\n\n<body>\n<div>\n    <h1>Example Domain</h1>\n    <p>This domain is established to be used for illustrative examples in documents. You may use this\n    domain in examples without prior coordination or asking for permission.</p>\n    <p><a href="http://www.iana.org/domains/example">More information...</a></p>\n</div>\n\n\n</body></html>"""

html_example_str_2 = """\n<html><head>\n    <title>Example Domain, another one</title>\n\n    <meta charset="utf-8">\n    <meta http-equiv="Content-type" content="text/html; charset=utf-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1">\n    <style type="text/css">\n    body {\n        background-color: #f0f0f2;\n        margin: 0;\n        padding: 0;\n        font-family: "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;\n\n    }\n    div {\n        width: 600px;\n        margin: 5em auto;\n        padding: 50px;\n        background-color: #fff;\n        border-radius: 1em;\n    }\n    a:link, a:visited {\n        color: #38488f;\n        text-decoration: none;\n    }\n    @media (max-width: 700px) {\n        body {\n            background-color: #fff;\n        }\n        div {\n            width: auto;\n            margin: 0 auto;\n            border-radius: 0;\n            padding: 1em;\n        }\n    }\n    </style>\n</head>\n\n<body>\n<div>\n    <h1>Example THIS Domain</h1>\n    <h3>HELLLOOOOOO</h3>\n    <style>h3 { background-color: #000; color: #333; }</style>\n    <p>This domain is established to be used for illustrative examples in documents. You may use this\n    domain in examples without prior coordination or asking for permission.</p>\n    <p><a href="http://www.iana.org/domains/example">More information...</a></p>\n    <input value="HELLO THERE"/>\n</div>\n\n\n</body></html>\n"""


script_str = "<script>some js stuff...</script>"
script_str_2 = "<script>some different js stuff...</script>"
script_str_3 = """<span class="important">this is important</span><script>some js stuff...</script>"""
script_str_4 = """<span class="important">this is changed</span><script>some different js stuff...</script>"""
