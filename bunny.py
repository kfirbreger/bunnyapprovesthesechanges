# Core
from random import choice
import HTMLParser
# Libs
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException  # , NotFound


class Bunny(object):

    def __init__(self):
        self.url_map = Map([
            Rule('/', endpoint='html'),
            Rule('/index.html', endpoint='html'),
            Rule('/txt', endpoint='txt'),
            Rule('/index.txt', endpoint='txt'),
            Rule('/py', endpoint='py'),
            Rule('/index.py', endpoint='py')
        ])
        self.bunnies = {
            'normal': '(O.o)',
            'cold': '(-.-)',
            'bigeye': '(O.O)',
            'smalleye': '(o.o)',
            'star': '(*.*)',
            'happy': '(^.^)',
            'stoned': '(@.@)',
            'misty': '(~.~)',
            'question': '(?.?)',
            'out': '(#.#)',
            'money': '($.$)',
            'closeeyed': '(V.V)',
            'visor': '(&laquo;.&raquo;)',
            'cross': '(&lsaquo;.&rsaquo;)',
            'roundeyed': '(&#702;.&#703;)',
        }
        self.messages = [
            'approves these changes', 'questions your changes', 'is surprised at your changes',
            "thinks it's just minor changes", 'is amazed at how awesome the changes are',
            'sees a bright future for these changes', 'smoked better changes', 'prefers not to look at these changes',
            'questions your changes', 'lost consciousness just looking at these changes',
            'thinks these changes will bring in the cheddar', 'happy, good change', 'sees dead changes',
            'just killed some bugs', 'visor shoots lasers, pew pew', 'finds your changes so boring, he just fell asleep',
            'is just speechless'
        ]
        self.matches = [
            ['normal', 0], ['cold', 1, 13], ['bigeye', 2], ['smalleye', 3], ['star', 4], ['happy', 5, 11],
            ['stoned', 6, 12], ['misty', 7], ['question', 8], ['out', 9], ['money', 10], ['visor', 14],
            ['closeeyed', 15], ['cross', 16], ['roundeyed', 16]
        ]

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, 'on_' + endpoint)(request, **values)
        except HTTPException, e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def on_html(self, request):
        bunny = u"""<!DOCTYPE html>
<html>
<head>
    <title>Commit Bunnies</title>
    <link rel="icon" type="image/png" href="bunnycon.png">
    <style>
    html, body, p, a{
        margin:0;
        padding:0;
        border:0;
    }
    body {
        font-family: 'Lucida Console', 'Courier New';
        font-size: 24pt;
        font-style: normal;
        letter-spacing: 0;
        line-height: 1.2;
        text-align: center;
        word-spacing: 0;
    }
    #content {
        width: 960px;
        margin: 1em auto;
        text-align:left;
    }
    #footer {
        position: fixed;
        bottom:12px;
        width: 100%;
        margin: 0 auto;
        text-align:center;
        font-size: 12pt;
        color: rgb(100,100,100);
        color: rgba(0,0,0, 0.5);
    }
    a {
        color: rgb(50,50,50);
        color: rgba(0,0,0, 0.8);
        text-decoration: none;
        font-weight:bold;
    }
    </style>
</head>

<body>
    <div id="content">
        <p>""" + self.chooseBunny('html') + """</p>
    </div>
    <div id="footer">
        <span>Totally inspired by <a href='http://whatthecommit.com/'>whatthecommit.com</a></span>
    </div>
</body>
</html>
"""
        return Response(bunny, mimetype='text/html')

    def on_txt(self, request):
        bunny = self.chooseBunny('txt')
        return Response(bunny)

    def on_py(self, request):
        bunny = "\"\"\"\n" + self.chooseBunny('py') + "\n\"\"\""
        return Response(bunny)

    def chooseBunny(self, format):
        chosen = choice(self.matches)
        bun = chosen[0]
        chosen = chosen[1:]
        msg = choice(chosen)
        bun = self.bunnies[bun]
        msg = self.messages[msg]
        specials = None
        if isinstance(bun, list):
            tmp = bun[0]
            bun = bun[1:]
            specials = bun
            bun = tmp
        return self.buildBunny(bun, msg, format, specials)

    def buildBunny(self, bun, message, format, specials=None):
        """
        Format is the format the bunny is in
        specials is a list. The first value is header, the second footer
        """
        header = '(\ /)'
        footer = '(> <)'
        glue = "\n"
        if format == 'html':
            footer = '(&gt; &lt;)'
        if specials is not None:
            header = specials[0]
            footer = specials[1]
        # Creating full footer
        footer += ' Bunny %s' % message
        if format == 'html':
            glue = "<br />"
        # Joining the bunny
        bunny = unicode(glue.join([header, bun, footer]))
        if format != 'html':
            h = HTMLParser.HTMLParser()
            bunny = h.unescape(bunny)
        return bunny


application = Bunny()
