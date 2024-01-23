# https://github.com/onaio/onadata/blob/79bf7c73faa4d56e1166ecc3a5bdc61086310ce8/onadata/libs/utils/common_tags.py#L175
# get data type by sampling submissions data
metadata_fields_type = {
    "_review_comment": "string",
    "_review_status": "string",
    "_status": "string",
    "_edited": "boolean",
    "_version": "string",
    "_duration": "string",
    "_notes": "array",
    "_uuid": "string",
    "_tags": "array",
    "_bamboo_dataset_id": "string",
    "_attachments": "array",
    "_geolocation": "array",
    "_media_count": "integer",
    "_total_media": "integer",
    "_submitted_by": "string",
    "_media_all_received": "boolean",
    "_xform_id_string": "string",
    "_submission_time": "string",
    "_xform_id": "integer",
    "_date_modified": "string",
}

# fields in submissions data but neither in xform nor metadata
extra_fields = {"_id": "string", "formhub/uuid": "string"}


def json_schema_from_metadata(metadata_types: dict) -> dict:
    """Generate a JSON schema from an ona data metadata dict."""
    schema_properties = {
        k: {
            "type": [
                # default to "string" then "null" types
                # in case lookup type is not compatible
                # e.g found a string "300%" instead of expected integer "300"
                # see issue here https://github.com/onaio/zebra/issues/7798
                "null",
                # *(["string"] if v != "string" else []),
                # default to "number" type
                # in case lookup type is of type integer
                # but underlying data is not compatible
                # e.g found data "-1.0" in a column of type integer
                # see issue here https://github.com/onaio/zebra/issues/7798
                # *(["number"] if v == "integer" else []),
                v,
            ]
        }
        for k, v in metadata_types.items()
    }

    return {"properties": schema_properties}
