from bson.json_util import dumps
from jsonschema import validate, ValidationError

class Validate:
    def validate_document(document, document_schema):
        try:
            validate(instance=document, schema=document_schema)
            return True
        except ValidationError as e:
            print(f"Validation error: {e}")
            return False