#!/usr/bin/env python3
"""A module for filtering logs.

This script connects to a MySQL database, retrieves user data, and logs it
while redacting sensitive personal information (PII) fields.
"""

import os
import re
import logging
import mysql.connector
from typing import List

# Regular expression patterns for extracting and replacing sensitive info
patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}

# List of fields considered as Personally Identifiable Information (PII)
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str,
        ) -> str:
    """Filters a log line by redacting specified fields.

    Args:
        fields (List[str]): List of fields to redact.
        redaction (str): The string used to replace sensitive data.
        message (str): The log message containing PII to be redacted.
        separator (str): Separator used in the log message.

    Returns:
        str: The redacted message.
    """
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


def get_logger() -> logging.Logger:
    """Creates and configures a logger to handle user data securely.

    Returns:
        logging.Logger: Configured logger with a redacting formatter.
    """
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    # Setting up formatter to redact specified PII fields
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Creates a MySQL database connection using environment variables.

    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object.
    """
    # Environment variables for database connection parameters
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    connection = mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )
    return connection


def main():
    """Fetches and logs user data from the database, redacting sensitive info

    Connects to the 'users' table and logs each user record while replacing
    PII fields with redacted content.
    """
    # Fields to retrieve from the 'users' table
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)
    info_logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        # Process each row to format and redact PII before logging
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row),
            )
            msg = '{};'.format('; '.join(list(record)))
            # Creating a log record with redacted information
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            info_logger.handle(log_record)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class to redact PII fields in logs."""

    REDACTION = "***"  # Redaction placeholder for sensitive fields
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    FORMAT_FIELDS = ('name', 'levelname', 'asctime', 'message')
    SEPARATOR = ";"  # Separator for log fields

    def __init__(self, fields: List[str]):
        """Initializes the formatter with fields to redact.

        Args:
            fields (List[str]): List of fields to redact in log messages.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats a log record with redacted PII fields.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The redacted log message.
        """
        msg = super(RedactingFormatter, self).format(record)
        # Apply redaction to PII fields in the log message
        txt = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt


if __name__ == "__main__":
    main()
