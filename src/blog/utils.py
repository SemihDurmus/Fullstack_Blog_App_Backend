import uuid


def get_random_code():
    code = str(uuid.uuid4())[:11].replace("-", "")
    # 4b2d3bcc-ec30-4716-9f63-55e8a4beeb5f ==> 4b2d3bccec
    return code


# print(get_random_code())
