from django.core.exceptions import ValidationError
import re


def validate_cpf(value):
    sequence_repeated_pattern = re.compile(r'\b(\d)\1{10}\b')

    if not re.match(r'\d{11}', value):
        raise ValidationError("A valid cpf must be entered in #1")

    if sequence_repeated_pattern.match(value):
        raise ValidationError("A valid cpf must be entered in #2")

    if not cpf(value):
        raise ValidationError("A valid cpf must be entered in #3")

    return value


def cpf(value):
    digit_first = (
        (sum(int(a) * b for a, b in zip(value[0:9], range(10, 1, -1)))) * 10 % 11
    )
    digit_second = (
        (sum(int(a) * b for a, b in zip(value[0:10], range(11, 1, -1)))) * 10 % 11
    )
    return str(digit_first) == value[-2] and str(digit_second) == value[-1]


def validate_phone(value):
    if not re.match(r'\d{11}', value):
        raise ValidationError("A valid telephone number must be entered in #1")
