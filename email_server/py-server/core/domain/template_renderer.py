from email import Email
from typing import Any
from template_catalog_enum import TemplateCatalogEnum


def render_template(template_name: TemplateCatalogEnum, fill_values: dict[str, Any]) -> Email:
    raise NotImplementedError("incomplete: function undefined")
