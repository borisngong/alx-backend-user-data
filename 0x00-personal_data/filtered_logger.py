#!/usr/bin/env python3
""" """

import re


def filter_datum(fields, redaction, message, separator):
    pattern = '|'.join([f'{field}=[^{separator}]*' for field in fields])
    return re.sub(pattern, lambda match: match.group().split('=')[0] + '='
                  + redaction, message)
