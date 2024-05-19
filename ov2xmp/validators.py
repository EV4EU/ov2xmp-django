import django
from django.core.validators import BaseValidator
from jsonschema.exceptions import ValidationError
from jsonschema import validate
from django.core.exceptions import ValidationError


class JSONSchemaValidator(BaseValidator):
    def compare(self, value, schema):
        try:
            validate(value, schema)
        except ValidationError:
            raise ValidationError(
                '%(value)s failed JSON schema check', params={'value': value}
            )
