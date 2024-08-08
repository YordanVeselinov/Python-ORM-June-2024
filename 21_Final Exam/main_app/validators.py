from django.core.exceptions import ValidationError


# class OnlyDigits:
#     def __call__(self, value: str):
#         if not value.isalpha():
#             raise ValidationError()
#
#     def deconstruct(self):
#         return (
#             'main_app.validators.OnlyDigits',
#             (),
#             {}
#         )


def only_digits_phone_number(value: str) -> ValidationError or None:
    if not value.isdigit():
        raise ValidationError()
