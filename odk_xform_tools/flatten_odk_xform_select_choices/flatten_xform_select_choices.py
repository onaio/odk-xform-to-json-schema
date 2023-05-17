from pyxform.aliases import control, select


def flatten_select_dictionary(select_dict):
    field = select_dict["name"]
    result = []

    for child in select_dict["children"]:
        value = child["name"]
        label = child["label"]

        if isinstance(label, dict):
            for language, label_value in label.items():
                result.append(
                    {
                        "field": field,
                        "value": value,
                        "language": language,
                        "label": label_value,
                    }
                )
        else:
            result.append(
                {
                    "field": field,
                    "value": value,
                    "language": "undefined",
                    "label": label,
                }
            )

    return result


def flatten_xform_select_choices(xform: dict) -> list:
    children = xform["children"]
    parsed_data = []

    for child in children:
        # get list of all possible select types from pyxform
        if select.get(child["type"]) is not None:
            parsed_data += flatten_select_dictionary(child)
        # check for nested control types (group, repeat, etc.)
        if control.get(child["type"]) is not None:
            parsed_data += flatten_xform_select_choices(child)

    return parsed_data
