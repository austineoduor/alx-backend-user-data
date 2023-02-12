#!/usr/bin/env python3
'''
0. Regex-ing
'''
from typing import List
import re
import logging


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    '''
    a function called filter_datum that returns the log message obfuscated:
    '''
    lists = message.split(separator)

    for field in fields:
        for j in range(len(lists)):
            if lists[j].startswith(field):
                strin = field + '=' + redaction
                lists[j] = re.sub(lists[j], '', lists[j])
                lists[j] = strin
    return separator.join(lists)


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ constructor """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ generates a log"""
        msg = logging.Formatter(self.FORMAT).format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    A function that takes no arguments and returns a logging.Logger object
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = RedactingFormatter(list(PII_FIELDS))
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
