from fastapi_utils.camelcase import camel2snake, snake2camel

assert snake2camel("some_field_name", start_lower=False) == "SomeFieldName"
assert snake2camel("some_field_name", start_lower=True) == "someFieldName"
assert camel2snake("someFieldName") == "some_field_name"
assert camel2snake("SomeFieldName") == "some_field_name"
