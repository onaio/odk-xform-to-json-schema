# ODK XForm Tools

This module does two things:

1. Parse an [ODK XForm](https://getodk.github.io/xforms-spec/) JSON representation (schema) into a [JSON Schema](https://json-schema.org/)
2. Parse an ODK XForm JSON representation (schema) to extract a flat select choices dictionary/table

## Testing

Run in the terminal with:

```bash
python main.py <function_name> <xform_file_path>

# e.g.
python main.py xform_to_json_schema sample_files/xform_example_1.json
```

Pipe output to a file with:

```bash
python main.py xform_to_json_schema sample_files/xform_example_1.json > sample_files/json_schema_example_1.json
python main.py flatten_xform_select_choices sample_files/xform_example_2.json > sample_files/select_choices_example_2.json
```
