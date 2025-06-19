import re

from mkdocs.plugins import BasePlugin


class OverwriteMath(BasePlugin):
    def on_post_page(self, output, /, *, page, config):
        output = re.sub(
            r'<span class="arithmatex">\\\(<span class="arithmatex">\\\(',
            r'<span class="arithmatex">\\(',
            output,
        )
        output = re.sub(r"\\\)</span>\\\)</span>", r"\\)</span>", output)
        return output
