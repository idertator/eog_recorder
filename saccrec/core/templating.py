from os.path import dirname, join, getmtime, exists

from jinja2 import BaseLoader, TemplateNotFound, Environment

from saccrec.settings import gui


class _TemplateLoader(BaseLoader):

    def __init__(self, *additional_paths):
        self._path = join(dirname(dirname(__file__)), 'templates')

    def get_source(self, environment, template):
        if template.endswith('.html'):
            filename = template
        else:
            filename = f'{template}_{gui.lang}.html'

        fullpath = join(self._path, filename)

        if not exists(fullpath):
            raise TemplateNotFound(template)

        mtime = getmtime(fullpath)

        with open(fullpath) as f:
            source = f.read()

        return source, self._path, lambda: mtime == getmtime(self._path)


_env = None


def render(template: str, **context) -> str:
    global _env
    if _env is None:
        _env = Environment(
            loader=_TemplateLoader()
        )

    template = _env.get_template(template)
    return template.render(
        lang=gui.lang,
        **context
    )
