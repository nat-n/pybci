import os
from tornado.web import RequestHandler

DIRECTORY_ROOT = os.path.dirname(__file__)
TEMPLATES_ROOT = os.path.join(DIRECTORY_ROOT, '../../client/templates/')
CLIENT_ROOT = os.path.join(DIRECTORY_ROOT, '../../client')

class Dashboard(RequestHandler):
    """
    Render single page app.
    """

    def _parse_slug(self, slug):
        result = {
          "path": "/",
          "query": "",
          "hash": ""
        }
        split_slug = slug.split('?', 2)
        result['path'] = split_slug[0]
        if len(split_slug) > 1:
            split_query = split_slug.split('#', 2)
            result['query'] = split_query[0]
            if len(split_query) > 1:
                result['hash'] = split_query[1]

        return result

    def do404(self):
        self.clear()
        self.set_status(404)
        self.finish("404")

    def get(self, slug):
        parsed_slug = self._parse_slug(slug)

        if ".." in parsed_slug['path']:
          self.do404()

        path = os.path.join(CLIENT_ROOT, parsed_slug['path'])

        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

        if len(parsed_slug['path']) < 2:
            html_path = os.path.join(TEMPLATES_ROOT + 'main.html')
            self.render(html_path)

        elif os.path.isfile(path):
            with open(path) as f:
                if "/css/" in path:
                    self.set_header("Content-Type", 'text/css; charset="utf-8"')
                elif "/js/" in path:
                    self.set_header("Content-Type", 'application/javascript; charset="utf-8"')
                self.write(f.read())
        else:
          self.do404()

