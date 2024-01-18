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
    schema_properties = {k: {"type": ["null", v]} for k, v in metadata_types.items()}

    return {"properties": schema_properties}
