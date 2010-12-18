from unittest import TestCase

from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES


class LocalFlavorTestCase(TestCase):
    def assertFieldOutput(self, fieldclass, valid, invalid, field_args=[],
        field_kwargs={}, empty_value=u''):
        """Asserts that a field behaves correctly with various inputs.

        Args:
            fieldclass: the class of the field to be tested.
            valid: a dictionary mapping valid inputs to their expected
                    cleaned values.
            invalid: a dictionary mapping invalid inputs to one or more
                    raised error messages.
            fieldargs: the args passed to instantiate the field
            fieldkwargs: the kwargs passed to instantiate the field
            emptyvalue: the expected clean output for inputs in EMPTY_VALUES
        """
        required = fieldclass(*field_args, **field_kwargs)
        optional = fieldclass(*field_args, required=False, **field_kwargs)
        # test valid inputs
        for input, output in valid.items():
            self.assertEqual(required.clean(input), output)
            self.assertEqual(optional.clean(input), output)
        # test invalid inputs
        for input, errors in invalid.items():
            try:
                required.clean(input)
            except ValidationError, e:
                self.assertEqual(errors, e.messages)
            else:
                self.fail()
            try:
                optional.clean(input)
            except ValidationError, e:
                self.assertEqual(errors, e.messages)
            else:
                self.fail()
        # test required inputs
        error_required = [u'This field is required.']
        for val in EMPTY_VALUES:
            try:
                required.clean(val)
            except ValidationError, e:
                self.assertEqual(error_required, e.messages)
            else:
                self.fail()
            self.assertEqual(optional.clean(val), empty_value)
