import json

from pyxform.question_type_dictionary import QUESTION_TYPE_DICT


def convert_xform_to_json_schema(xform: dict) -> str:
    """Generate a `JSON Schema` from an `ODK XForm Schema`.

    This function parses an ODK XForm schema in JSON format
    and generates a corresponding compliant JSON schema.
    It does this by traversing the XForm schema and
    mapping XForm native question types to `JSON Schema` types.


    Parameters
    ----------
    xform : Dict
        An XForm in JSON format

    Returns
    -------
    JSON string
        A JSON Schema JSON string

    Example
    --------
    >>> convert_xform_to_json_schema({"children":[{"name":"start","type":"start"}]})
    """

    xform_question_name_to_question_type = {
        k: v.get("bind", {}).get("type", "string")
        for k, v in QUESTION_TYPE_DICT.items()
    }

    # set(xform_question_name_to_question_type.values())
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

    xform_type_to_json_schema_type_mapper = {
        k: xform_type_to_json_schema_type.get(v, "string")
        for k, v in xform_question_name_to_question_type.items()
    }

    def get_child_properties(children, path="") -> list[dict]:
        """Convert children properties and types to JSON Schema properties format

        Recursively concat paths for nested groups


        Parameters
        ----------
        children : List
        An XForm children property - or any nested xform children property

        Returns
        -------
        List[Dict]
        A list of JSON Schema properties (dictionaries)

        Example
        --------
        >>> get_child_properties([{"name":"start","type":"start"}])
        """
        schema_properties = []
        for child in children:
            child_name = child.get("name")
            child_type = child.get("type")
            child_path = f"{path}/{child_name}" if path else child_name
            if child_type == "group":
                schema_properties += get_child_properties(child["children"], child_path)
            elif child_type == "repeat":
                repeat_group = {
                    child_path: {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                k: v
                                for prop in get_child_properties(
                                    child["children"], child_path
                                )
                                for k, v in prop.items()
                            },
                        },
                    }
                }
                schema_properties.append(repeat_group)
            else:
                child_lookup_type = xform_type_to_json_schema_type_mapper.get(
                    child["type"], "string"
                )
                schema_properties.append({child_path: {"type": child_lookup_type}})
        return schema_properties

    # json_schema_template["properties"] = {
    #     k: v for d in get_child_properties(xform["children"]) for k, v in d.items()
    # }

    def compose_json_schema_properties(schema_properties: list[dict]):
        json_schema_template = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {},
        }
        # for schema_property in schema_properties:
        #     json_schema_template["properties"].update(schema_property)
        json_schema_template["properties"] = {
            k: v for d in schema_properties for k, v in d.items()
        }
        return json_schema_template

    schema_properties = get_child_properties(xform["children"])

    return json.dumps(compose_json_schema_properties(schema_properties), indent=2)
