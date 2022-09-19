import os
import hashlib
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import json
import base64
 
def is_nan(val):
    """ Returns  true if value is nan.

    :param value: value to be checked
    :return: value
    :rtype: boolean
    """
    return val != val
            
def hash_text(text,seed):
    """ Hash a value . The value  will be hashed using sha256 algorithm
    and  a seed

    :param text: value to be hashed
    :return: hashed value
    :rtype: string
    """
    if is_nan(text):
        return None
    else: 
        seed_utf8 = (seed.encode('utf-8')).hex()
        return hashlib.sha256(seed_utf8.encode() + str(text).encode()).hexdigest()

def date_shift(in_date_to_shift,seed) :
    """ Shift a date from a string date.

    :param in_date_to_shift: date to be shifted
    :return: shifted_date
    :rtype: datetime
    """
    if is_nan(in_date_to_shift):
        return None

    else:
        in_date_to_shift = str(in_date_to_shift)
        shift_base = 366
        hashed_value = hash_text(in_date_to_shift,seed)
        hash_list = [ord(x) for x in hashed_value]
        num_list =  [i for n, i in enumerate(hash_list) if i not in hash_list[:n]]
        num_list.sort()
        for number in num_list:
            nrb_days = int(str('%.3f' % (number/shift_base)).split('.')[1])
            if nrb_days < 366  and nrb_days > 99:
                break
            else:
                nrb_days = shift_base
        shifted_date = deserialize_date(in_date_to_shift) + relativedelta(days=nrb_days)
        return shifted_date 

def deserialize_date(string):
    """Deserializes string to date.

    :param string: str.
    :return: date.
    """
    if string is None:
        return None
    else:
        return parse(string)