from django.core.exceptions import ValidationError
import re


# CPF Validator
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


# Phone validator
ddd_valid = {
    'SP': ['11', '12', '13', '14', '15', '16', '17', '18', '19'],
    'RJ': ['21', '22', '24', '25', '26'],
    'ES': ['27', '28', '29'],
    'MG': ['31', '32', '33', '34', '35', '36', '37', '38', '39'],
    'PR': ['41', '42', '43', '44', '45', '46'],
    'SC': ['47', '48', '49'],
    'RS': ['51', '52', '53', '54', '55', '56', '59'],
    'DF': ['61'],
    'GO': ['61', '62', '64'],
    'TO': ['63'],
    'MT': ['65', '66'],
    'MS': ['67'],
    'AC': ['68'],
    'RO': ['69'],
    'BA': ['71', '72', '73', '74', '75', '76', '77', '78'],
    'SE': ['79'],
    'PE': ['81', '87'],
    'AL': ['82'],
    'PB': ['83'],
    'RN': ['84'],
    'CE': ['85', '88'],
    'PI': ['86', '89'],
    'PA': ['91', '93', '94'],
    'AM': ['92', '97'],
    'RR': ['95'],
    'AP': ['96'],
    'MA': ['98', '99'],
}


def validate_phone(value):

    # only numbers
    if not(value.isdigit()):
        raise ValidationError("A valid telephone must be numeric in #1")

    # two digits must be validated
    valid = False
    for key, val in ddd_valid:
        if value[:2] in val:
            valid = True
            break

    if not(valid):
        raise ValidationError("A valid DDD telephone must be entered in #2")

    # Amount of digits
    if not(re.match(r'\d{10}', value)) or not(re.match(r'\d{11}', value)):
        raise ValidationError("A valid 10 or 11 digit telephone must be entered in #3")
