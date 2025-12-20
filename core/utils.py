from drf_spectacular.utils import extend_schema, extend_schema_view
from json import dumps


def create_view_schema(schemaName: str, methods: list):
    extend_schema_list = {}
    for method in methods:
        extend_schema_list[method] = extend_schema(tags=[schemaName])
    schema = extend_schema_view(**extend_schema_list)
    return schema


def create_viewset_schema(schemaName):
    schema = extend_schema_view(
        create=extend_schema(tags=[schemaName]),
        destroy=extend_schema(tags=[schemaName]),
        update=extend_schema(tags=[schemaName]),
        list=extend_schema(tags=[schemaName]),
        retrieve=extend_schema(tags=[schemaName]),
        partial_update=extend_schema(tags=[schemaName]),
    )

    return schema


def json_serializer(data):
    return dumps(data).encode("utf-8")
