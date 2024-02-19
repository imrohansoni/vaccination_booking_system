import re

ALLOWED_IMAGE_EXTENSIONS = ["PNG", "JPEG", "JPG"]


class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors


class Validator:
    def __init__(self, obj, files=None):
        self.obj = obj
        self.files = files or {}
        self.errors = {}
        self.data = {}
        self.current_field = None

    def _get_field_value(self):
        if self.current_field is None:
            return self
        field = self.current_field
        return self.data.get(field)

    def _set_error(self, message):
        self.errors[self.current_field] = message

    def _is_type(self, type_name, message):
        field_value = self._get_field_value()
        if field_value is not None and not isinstance(field_value, type_name):
            self._set_error(message)
        return self

    def _get_length(self):
        current_field = self._get_field_value()
        if current_field is None or (current_field is not None and not isinstance(current_field, str)):
            return -1
        else:
            return len(current_field)

    def field(self, field_name):
        self.current_field = field_name

        if field_name in self.obj and self.obj[field_name] is not None and self.obj[field_name] != "":
            self.data[field_name] = self.obj[field_name]

        return self

    def required(self, message):
        field_value = self._get_field_value()
        if field_value is None:
            self._set_error(message)
        return self

    def match_pattern(self, regex, message):
        field_value = self._get_field_value()
        if field_value is None:
            return self
        if not re.match(regex, str(field_value)):
            self._set_error(message)
        return self

    def is_one_of(self, values, message):
        field_value = self._get_field_value()
        if field_value is None or not isinstance(values, list):
            return self
        if field_value not in values:
            self._set_error(message)
        return self

    def min_length(self, length, message):
        str_length = self._get_length()
        if str_length < 0:
            return self
        if str_length < length:
            self._set_error(message)
        return self

    def max_length(self, length, message):
        str_length = self._get_length()
        if str_length < 0:
            return self
        if str_length > length:
            self._set_error(message)
        return self

    def range_length(self, min_length, max_length, message):
        str_length = self._get_length()
        if str_length < min_length or str_length > max_length or str_length < 0:
            self._set_error(message)
        return self

    def is_number(self, message):
        self._is_type(int, message)
        return self

    def is_string(self, message):
        self._is_type(str, message)
        return self

    def is_bool(self, message):
        self._is_type(bool, message)
        return self

    def is_list(self, message):
        self._is_type(list, message)
        return self

    def is_list_empty(self, message):
        field_value = self._get_field_value()
        if field_value is None or not isinstance(field_value, list):
            return self
        if len(field_value) < 1:
            self._set_error(message)
        return self

    def is_dict(self, message):
        self._is_type(dict, message)
        return self

    def validate(self, callback, message):
        field_value = self._get_field_value()
        if field_value is None:
            return self
        result = callback(field_value)
        if not result:
            self._set_error(message)
        return self
