from binascii import b2a_hex, a2b_hex
import sqlalchemy.types as types

from xraspberry import config
from xraspberry.rasplife.common.crypt import aes_decrypt, aes_encrypt

encrypt_key = config.get_config("rasplife.data_key", "key")


class EncryptString(types.TypeDecorator):  # pylint: disable=W0223
    impl = types.String

    def process_bind_param(self, value, dialect):
        if not value:
            return value
        value = aes_encrypt(value.encode("utf-8"), key=encrypt_key, fill=True)
        value = b2a_hex(value)
        return value

    def process_result_value(self, value, dialect):
        if not value:
            return value
        res_value = aes_decrypt(a2b_hex(value), key=encrypt_key, strip=True)
        return res_value.decode("utf-8")
