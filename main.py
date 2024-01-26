import json
import sys

from odk_xform_tools import flatten_xform_select_choices, xform_to_json_schema


def main():
    """
    Run in the terminal with:
    python main.py <function_name> <xform_file_path>
    e.g. python main.py xform_to_json_schema sample_files/xform_example_1.json

    Pipe output to a file with:
    python main.py xform_to_json_schema sample_files/xform_example_1.json > sample_files/json_schema_example_1.json
    python main.py flatten_xform_select_choices sample_files/xform_example_2.json > sample_files/select_choices_example_2.json
    """

    # second argument should be the path to the xform file
    x_form_file = sys.argv[2]

    with open(x_form_file) as f:
        x_form_example = json.load(f)

    # first argument should be the function to run
    match sys.argv[1]:
        case "flatten_xform_select_choices":
            print(json.dumps(flatten_xform_select_choices(x_form_example), indent=2))
        case "xform_to_json_schema":
            print(json.dumps(xform_to_json_schema(x_form_example), indent=2))
        case _:
            print("Invalid function name")


if __name__ == "__main__":
    main()
