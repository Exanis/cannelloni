# -*- coding: utf8 -*-

"Convertor for scalar type"

def integer_convertor(target):
    "Convert a variable to integer"
    if target == '':
        return 0
    return int(target)

def float_convertor(target):
    "Convert a variable to float"
    if target == '':
        return 0.0
    return float(target)
