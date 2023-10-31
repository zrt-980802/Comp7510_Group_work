import binascii
from pyDes import des, CBC, PAD_PKCS5

password_certificate = "12345678"


def desEncrypt(s, secret_key=password_certificate):
    """
    加密
    :param secret_key:
    :param s:
    :return:
    """
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    return str(binascii.b2a_hex(en))


def desDecrypt(s, secret_key=password_certificate):
    """
    解密
    :param secret_key:
    :param s:
    :return:
    """
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    return de
