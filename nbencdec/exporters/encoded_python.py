"""Python script Exporter class"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import copy
import json
import os

from jupyter_core.paths import jupyter_path
from traitlets import default, validate

from nbconvert.exporters.templateexporter import TemplateExporter
from .filters import comment_lines_with_escaping, ipython2encodedpython


def strip_cells(notebook):
    clone = copy.deepcopy(notebook)
    del clone['cells']
    return json.dumps(clone, sort_keys=True)


class EncodedPythonExporter(TemplateExporter):
    """
    Exports a Python code file.
    """
    @validate('template_data_paths')
    def _add_template_path(self, proposal):
        """
        We want to inherit from HTML template, and have template under
        `./templates/` so append it to the search path. (see next section)
        """
        our_path = os.path.join(os.path.dirname(__file__), "templates")
        base_paths = jupyter_path("nbconvert", "templates", "base")
        if our_path not in proposal['value']:
            proposal['value'].append(our_path)
        for base_path in base_paths:
            if base_path not in proposal['value']:
                proposal['value'].append(base_path)
        return proposal['value']

    def default_filters(self):
        filters = list(super().default_filters())
        filters.append(("comment_lines_with_escaping", comment_lines_with_escaping))
        filters.append(("ipython2encodedpython", ipython2encodedpython))
        return filters

    @default('file_extension')
    def _file_extension_default(self):
        return '.py'

    @default('template_file')
    def _template_file_default(self):
        return 'encoded_python.tpl'

    def _init_resources(self, resources=None):
        resources = super(EncodedPythonExporter, self)._init_resources(resources)
        resources['strip_cells'] = strip_cells
        return resources

    output_mimetype = 'text/x-python'
