from marshmallow import Schema, fields

def image_validation(image):
    return all([
        ":" in image
    ])

class AutobuildSchema(Schema):
    """
        buildpack: The buildpack to build with
        name: The name of the image, and where to push it
    """
    # TODO: Define missing field for buildpack, should be one that can auto detect image
    buildpack = fields.Str()

    # TODO: Add in image validation for autobuild name field.
    name = fields.Str(required=True)

class StageSchema(Schema):
    # TODO: This is only valid if it's a valid image name
    image = fields.Str(missing="debian:stable-slim")
    script = fields.List(fields.Str(), required=True)
    autobuild = fields.Nested(AutobuildSchema, data_key="auto-build", validate=image_validation)
