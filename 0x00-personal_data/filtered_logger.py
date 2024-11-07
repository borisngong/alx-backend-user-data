#!/usr/bin/env python3
"""A module for filtering logs."""

import os
import re
import logging
from typing import List

# Define PII_FIELDS constant with sensitive fields
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class for sensitive data"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        # Format the log record message using the base class format
        original_message = super().format(record)
        # Redact sensitive information
        redacted_message = filter_datum(self.fields,
                                        self.REDACTION,
                                        original_message,
                                        self.SEPARATOR)
        return redacted_message


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Responsible for Filtering a log line.
    """
    pattern = r'(?P<field>{})=[^{}]*'.format('|'.join(fields), separator)
    return re.sub(pattern, r'\g<field>={}'.format(redaction), message)


def get_logger() -> logging.Logger:
    """Creates a logger for user data with a RedactingFormatter"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create a stream handler with the RedactingFormatter
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))

    # Attach the handler to the logger
    logger.addHandler(stream_handler)

    return logger
