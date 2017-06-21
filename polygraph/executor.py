from collections import OrderedDict

from attr import attrib, attributes
from graphql.language.ast import (
    Document,
    Field,
    FragmentSpread,
    FragmentDefinition,
    InlineFragment,
    SelectionSet,
)
from typing import Mapping


@attributes
class ExecutionResult:
    data = attrib()
    errors = attrib()


def field_response_key(field: Field) -> str:
    return field.alias or field.name


def document_fragments(document: Document) -> Mapping[str, FragmentDefinition]:
    # TODO:
    pass


def collect_fields(
    object_type,
    selection_set: SelectionSet,
    variable_values,
    visited_fragments,
    document_fragments,
):
    visited_fragments = visited_fragments or set()
    grouped_fields = OrderedDict()
    for selection in selection_set.selections:
        # TODO: @skip directive
        # TODO: @include directive
        if isinstance(selection, Field):
            response_key = field_response_key(selection)
            grouped_fields.setdefault(response_key, list())
            grouped_fields[response_key].append(selection)
        elif isinstance(selection, FragmentSpread):
            frag_spread_name = selection.name
            if frag_spread_name in visited_fragments:
                continue
            visited_fragments.add(frag_spread_name)
            fragment = document_fragments.get(frag_spread_name)
            if not fragment:
                continue
            fragment_group_field_set = collect_fields(object_type, fragment.selection_set, variable_values, document_fragments)


