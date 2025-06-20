#  Copyright (C) 2022-2025 Theodore Chang
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
