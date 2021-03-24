from datetime import datetime
from django.contrib.auth.hashers import make_password
from exceptions.cargo_details_exception import CargoDetailsException , CargoDetailsError
import base64
import hashlib
import pytz
import uuid


def serializer_error_to_string(errors):
    error_list = []
    for key, val in errors.items():
        if type(val) == list:
            if isinstance(val[0], dict):
                inner_errors = [serializer_error_to_string(item) for item in val]
                error_list += [error for error in inner_errors if error != '']
            else:
                error = "{} - {}".format(key, "".join(val))
                error_list.append(error)
    return ",".join(error_list)


def set_default_none(data, fields):
    for field in fields:
        if field.name not in data:
            data[field.name] = None

    return data

# Generate token by concatenating data with uuid delimeted by '__' (double underscore)
def generate_token(email,type=None):
    token = uuid.uuid4()
    token_hash = email+ '__'
    if type is not None:
        token_hash = token_hash + type +'__'

    token_hash = token_hash + str(token)

    return token_hash, token


# Encode data using b64decode library
def encode_data(data):
    data_to_bytes = data.encode('ascii')
    data_base64_bytes = base64.b64encode(data_to_bytes)
    base64_data = data_base64_bytes.decode('ascii')

    return base64_data

# Decode data using b64decode library
def decode_data(data):
    data_base64_bytes = data.encode('ascii')
    data_bytes = base64.b64decode(data_base64_bytes)
    decoded_data = data_bytes.decode('ascii')

    return decoded_data

# Calculate number of days between 2 dates
def date_diffs_in_hours(date1, date2):
    date1 = datetime.strptime(date1, "%Y-%m-%dT%H:%M:%S.%fZ")
    date2 = datetime.strptime(date2.strftime("%Y-%m-%d"), "%Y-%m-%d")
    return abs((date2 - date1).days) * 24

# Calculate number of hours between 2 dates
def date_difference_in_hours(date1, date2):
    time_delta = (date2 - date1).total_seconds()
    hours=time_delta/3600
    return hours

# Generate token and encode token using email
def generate_token_data(email,type=None):
    token_hash, token  = generate_token(email,type)
    encoded_token_hash = encode_data(token_hash)

    return encoded_token_hash, token

# Encode password using MD5, SHA256 and DJANFO AUTH Make Password Hash
def encode_password(password):
    encode_md5 = hashlib.md5(password.encode()).hexdigest()
    encode_sha1 = hashlib.sha256(encode_md5.encode()).hexdigest()
    return encode_sha1


def present_or_future_date(value):

    tz_IN = pytz.timezone('Asia/Kolkata')
    datetime_IN = datetime.now(tz_IN)
    dt = datetime_IN.strftime("%m/%d/%Y")

    current_date = datetime.strptime(dt, '%m/%d/%Y').date()

    if value < current_date:
        raise CargoDetailsException(CargoDetailsError.INVALID_DATE)
    return value


def Diff(li1, li2):
    return (list(set(li1) - set(li2)))


def unique(list1):
    # insert the list to the set
    list_set = set(list1)
    # convert the set to the list
    unique_list = (list(list_set))

    return unique_list;
