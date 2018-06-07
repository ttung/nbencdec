{%- extends 'null.tpl' -%}

{%- block header -%}
#!/usr/bin/env python
# coding: utf-8
#
# EPY: stripped_notebook: {{ resources.strip_cells(nb) }}
{% endblock header %}

{% block input %}
# EPY: START code
{{ cell.source | ipython2encodedpython -}}
# EPY: END code
{% endblock input %}

{% block markdowncell scoped %}
# EPY: START markdown
{{ cell.source | comment_lines_with_escaping }}
# EPY: END markdown
{% endblock markdowncell %}
