from pyxform import QUESTION_TYPE_DICT, constants
from pyxform.aliases import control

from .metadata_schema import (
    extra_fields,
    json_schema_from_metadata,
    metadata_fields_type,
)


def get_xform_type_to_json_schema_type_lookup():
    xform_q_name_to_q_type = {
        k: v.get("bind", {}).get("type", "string")
        for k, v in QUESTION_TYPE_DICT.items()
    }

    # set(xform_q_name_to_q_type.values())
    xform_type_to_json_schema_type = {
        "string": "string",
        "int": "integer",
        "decimal": "number",
        "time": "string",
        "date": "string",
        "dateTime": "string",
        "binary": "string",
        "barcode": "string",
        "odk:rank": "integer",
        "geoshape": "string",
        "geotrace": "string",
        "geopoint": "string",
    }

    return {
        k: xform_type_to_json_schema_type.get(v, "string")
        for k, v in xform_q_name_to_q_type.items()
    }


def get_schema_properties(
    xform,
    path="",
    xform_type_to_json_schema_type_lookup=get_xform_type_to_json_schema_type_lookup(),
) -> list[dict]:
    children = xform["children"]
    schema_properties = []

    for child in children:
        child_name = child["name"]
        child_path = f"{path}/{child_name}" if path else child_name
        child_control_type = control.get(child["type"])

        # nested control types (group, repeat, loop, etc.)
        # N/B: child_control_type == constants.LOOP not handled
        if child_control_type is not None:
            nested_properties = get_schema_properties(child, child_path)

            if child_control_type == constants.GROUP:
                schema_properties += nested_properties

            elif child_control_type == constants.REPEAT:
                schema_properties.append(
                    {
                        child_path: {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    k: v
                                    for prop in nested_properties
                                    for k, v in prop.items()
                                },
                            },
                        }
                    }
                )

        else:
            schema_properties.append(
                {
                    child_path: {
                        "type": xform_type_to_json_schema_type_lookup.get(
                            child["type"], "string"
                        )
                    }
                }
            )
    return schema_properties


def xform_to_json_schema(xform: dict, include_meta_data: bool = True):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            k: v for prop in get_schema_properties(xform) for k, v in prop.items()
        },
    }

    if include_meta_data:
        schema["properties"].update(
            json_schema_from_metadata({**metadata_fields_type, **extra_fields})[
                "properties"
            ]
        )

    return schema
