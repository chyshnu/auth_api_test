import base64
import random
import string
import hashlib
import json

from Crypto.Cipher import AES
from auth_api_test.exception.base import ApiException
from auth_api_test.exception.error import *
from auth_api_test.api.utils import make_timestamp, make_nonce


class SHA1:
    """消息签名接口"""

    @staticmethod
    def get_sha1(*args):
        """SHA1算法生成签名"""
        sortlist = list(args)
        sortlist.sort()
        # print(sortlist)

        try:
            sha = hashlib.sha1("".join(sortlist).encode('utf-8'))
            return sha.hexdigest()

        except Exception as e:
            # print(e)
            raise ApiException(Crypt_ComputeSignature_Error, suffix=str(e))


class JsonParse:
    """提供提取消息格式中的密文及生成回复消息格式的接口"""

    @classmethod
    def extract(cls, jsontext):
        """提取出json数据包中的加密消息
        @param jsontext: 待提取的json字符串
        @return: 提取出的加密消息字符串
        """
        try:
            json_dict = json.loads(jsontext)
            return json_dict
        except Exception as e:
            return ApiException(Crypt_ParseJson_Error, suffix=str(e))

    @classmethod
    def generate(cls, encrypt, signature, timestamp, nonce):
        """生成json消息
        @param encrypt: 加密后的消息密文
        @param signature: 安全签名
        @param timestamp: 时间戳
        @param nonce: 随机字符串
        @return: 生成的json字符串
        """
        resp_json = {
            'encrypt': encrypt,
            'signature': signature,
            'timestamp': timestamp,
            'nonce': nonce,
        }
        return resp_json


class PKCS7Encoder:
    """提供基于PKCS7算法的加解密接口"""

    block_size = 32

    def encode(self, text):
        """ 对需要加密的明文进行填充补位
        @param text: 需要进行填充补位操作的明文
        @return: 补齐明文字符串
        """
        text_length = len(text)
        # 计算需要填充的位数
        amount_to_pad = self.block_size - (text_length % self.block_size)
        if amount_to_pad == 0:
            amount_to_pad = self.block_size
        # 获得补位所用的字符
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    def decode(self, decrypted):
        """删除解密后明文的补位字符
        @param decrypted: 解密后的明文
        @return: 删除补位字符后的明文
        """
        # pad = ord(decrypted[-1])
        pad = decrypted[-1]  # pad = ord(chr(decrypted[-1]))
        if pad < 1 or pad > self.block_size:
            pad = 0
        return decrypted[:-pad]


class Prpcrypt:
    """消息加解密接口"""

    def __init__(self, key, iv):
        self.key = key.encode('utf-8')
        self.iv = iv.encode('utf-8')
        # 设置加解密模式为AES的CBC模式
        self.mode = AES.MODE_CBC
        self.pkcs7 = PKCS7Encoder()

    def encrypt(self, text):
        """对明文进行加密
        @param text: 需要加密的明文
        @return: 加密得到的字符串
        """
        # 16位随机字符串添加到明文开头
        text = self.get_random_str() + text
        # 使用自定义的填充方式对明文进行补位填充
        text = self.pkcs7.encode(text)
        # 加密
        cryptor = AES.new(self.key, self.mode, self.iv)
        try:
            # 使用BASE64对加密后的字符串进行编码
            ciphertext = base64.b64encode(cryptor.encrypt(text.encode('utf-8')))
            return str(ciphertext, 'utf-8')
        except Exception as e:
            raise ApiException(Crypt_EncryptAES_Error, suffix=str(e))

    def decrypt(self, text):
        """对解密后的明文进行补位删除
        @param text: 密文
        @return: 删除填充补位后的明文
        """
        try:
            cryptor = AES.new(self.key, self.mode, self.iv)
            # 使用BASE64对密文进行解码，然后AES-CBC解密
            plain_text = cryptor.decrypt(base64.b64decode(text))
        except Exception as e:
            raise ApiException(Crypt_DecryptAES_Error, suffix=str(e))
        try:
            decrypt_text = str(self.pkcs7.decode(plain_text), 'utf-8')[16:]
        except Exception as e:
            raise ApiException(Crypt_IllegalBuffer, suffix=str(e))
        return decrypt_text

    @staticmethod
    def get_random_str():
        """ 随机生成16位字符串
        @return: 16位字符串
        :return:
        """
        rule = string.ascii_letters + string.digits
        rndtxt = random.sample(rule, 16)
        return "".join(rndtxt)


class BizMsgCrypt:

    def __init__(self, token, AESKey, salt):
        self.token = token
        self.salt = salt
        self.pc = Prpcrypt(AESKey[:16], salt[:16])  # salt前16位作iv

    @staticmethod
    def verify_url(msg_sign, *args):
        compute_sign = SHA1.get_sha1(*args)
        return msg_sign == compute_sign

    def encryptMsg(self, plan_text, nonce=None, timestamp=None):
        encrypt_text = self.pc.encrypt(plan_text)
        if nonce is None:
            nonce = make_nonce()
        if timestamp is None:
            timestamp = make_timestamp()
        signature = SHA1.get_sha1(self.token, timestamp, nonce, self.salt, encrypt_text)
        return JsonParse.generate(encrypt_text, signature, timestamp, nonce)

    def decryptMsg(self, encrypt_text):
        json_content = self.pc.decrypt(encrypt_text)
        return JsonParse.extract(json_content)
