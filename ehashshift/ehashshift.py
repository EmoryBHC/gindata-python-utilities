import os
import hashlib
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import json
import boto3
import base64
from botocore.exceptions import ClientError



def get_secret():

    secret_name = 'NeuroCEPSeeddev'
    region_name = os.environ['AWS_REGION']

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
  
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            raise e
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        return secret
 
def isNaN(val):
    """ Returns  true if value is nan.

    :param value: value to be checked
    :return: value
    :rtype: boolean
    """
    return val != val
            

def hashText(text):
    """ Hash a value . The value  will be hashed using sha256 algorithm
    and  a seed from AWS secrets

    :param text: value to be hashed
    :return: hashed value
    :rtype: string
    """
    if isNaN(text):
        return None
    else: 
        secrets = json.loads(get_secret())
        seed_key = secrets['Seed']
        seed = (seed_key.encode('utf-8')).hex()
        return hashlib.sha256(seed.encode() + str(text).encode()).hexdigest()


def date_shift(in_date_to_shift) :
    """ Shift a date from a string date.

    :param in_date_to_shift: date to be shifted
    :return: shifted_date
    :rtype: datetime
    """
    if isNaN(in_date_to_shift):
        return None

    else:
        in_date_to_shift = str(in_date_to_shift)
        shift_base = 366
        hashed_value = hashText(in_date_to_shift)
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
