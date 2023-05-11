from pyxform import QUESTION_TYPE_DICT, constants
from pyxform.aliases import control


# TODO: re-look at the best naming conventions for this module:
# function names, variable names, module name etc
# TODO: update docstring
def xform_to_json_schema(xform: dict):
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
    >>> xform_to_json_schema({"children":[{"name":"start","type":"start"}]})
    """

    xform_q_name_q_type_dict = {
        k: v.get("bind", {}).get("type", "string")
        for k, v in QUESTION_TYPE_DICT.items()
    }

    # TODO: get forms that use these types to see their representations
    # TODO: confirm these types map to JSON Schema types seamlessly
    # set(xform_q_name_q_type_dict.values())
    xform_to_json_schema_type = {
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

    xform_to_json_schema_type_mapper = {
        k: xform_to_json_schema_type.get(v, "string")
        for k, v in xform_q_name_q_type_dict.items()
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
            child_path = f"{path}/{child_name}" if path else child_name
            child_control_type = control.get(child.get("type"))

            # TODO: is constants.LOOP comparable to constants.REPEAT?
            # nested control groups
            if child_control_type in (constants.GROUP, constants.REPEAT):
                nested_properties = get_child_properties(child["children"], child_path)

                if child_control_type == constants.GROUP:
                    schema_properties += nested_properties
                # TODO: child_control_type in (constants.REPEAT, constants.LOOP):
                elif child_control_type == constants.REPEAT:
                    repeat_group = {
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
                    schema_properties.append(repeat_group)
            else:
                schema_properties.append(
                    {
                        child_path: {
                            "type": xform_to_json_schema_type_mapper.get(
                                child["type"], "string"
                            )
                        }
                    }
                )
        return schema_properties

    def compose_json_schema_properties(schema_properties: list[dict]):
        json_schema_template = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {k: v for prop in schema_properties for k, v in prop.items()},
        }
        return json_schema_template

    return compose_json_schema_properties(get_child_properties(xform["children"]))
