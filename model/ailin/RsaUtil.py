
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.PublicKey.RSA import RsaKey

class RsaUtil(object) :
    def format_key(self,key):
        if not isinstance(key, RsaKey):
            # ValueError: RSA key format is not supported
            if not key.startswith('-----') and not key.endswith('-----'):
                key = '-----BEGIN KEY-----\n%s\n-----END KEY-----' % key
            key = RSA.importKey(key)
        return key

    # 加密
    def long_encrypt(self,public_key, msg):
        public_key = self.format_key(public_key)
        msg = msg.encode('utf-8')
        length = len(msg)
        default_length = 117
        # 公钥加密
        pubobj = PKCS1_cipher.new(public_key)
        # 长度不用分段
        if length < default_length:
            return base64.b64encode(pubobj.encrypt(msg)).decode('utf-8')
        # 需要分段
        offset = 0
        res = []
        while length - offset > 0:
            if length - offset > default_length:
                res.append(pubobj.encrypt(msg[offset:offset + default_length]))
            else:
                res.append(pubobj.encrypt(msg[offset:]))
            offset += default_length
        byte_data = b''.join(res)
        return base64.b64encode(byte_data).decode('utf-8')

    # 解密
    def long_decrypt(self,private_key, msg):
        private_key = self.format_key(private_key)
        msg = base64.b64decode(msg)
        length = len(msg)
        default_length = 128
        # 私钥解密
        priobj = PKCS1_cipher.new(private_key)
        # 长度不用分段
        if length < default_length:
            return b''.join(priobj.decrypt(msg, b'xyz'))
        # 需要分段
        offset = 0
        res = []
        while length - offset > 0:
            if length - offset > default_length:
                res.append(priobj.decrypt(msg[offset:offset + default_length], b'xyz'))
            else:
                res.append(priobj.decrypt(msg[offset:], b'xyz'))
            offset += default_length
        return b''.join(res).decode('utf8')
    pass




if __name__ == '__main__':
    RsaUtil = RsaUtil()
    peo="MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAKAxk9iEKPRDUqI/N4mkA0vZ2fQ7DGLpKwmrtePh0aPAdrbIztoMpi5WDPmHapy4+Irt/FFBvOn4l0MvCh86iuWeSWM8H0f8LudRCxC4rStCT0ugnJd3TBAE0HdcgOsJKB6X5KxZieMWoBHs9MxDgx81PZzIjTdtG6BPQR1YlFezAgMBAAECgYBH/sAhmRQG45Lp1FuTgqDwoBIyj687bOuoxwFST5U2cTNpZsqAeRrezFG8e73QfdlGJzs1EcRjqxPgX+2+p0LwxGhkhifFviH8Dc51lhNd+jZV+5W2Q854sxYMdYkrRFvr9m8c4Pno2geHnNIclr18e/CehLOh4WF4dVV0+j8R8QJBAOQP0yUyWKZ7JXcRmgfBEpf/xhWNQaxHbYzK8jjaciCXDoZV85WAVB5NOTv/N4Q96SlYXcOE41hd/hCahMrkMu8CQQCz0VxeyNBXddHhZH8MNa2kPcEme/r8/OmEZEvdoneb3MNaqUWIaBs3hmhb6A/qe+M0MnmbPPEcTtpijCdSrBd9AkBq0oK69IcTi7DzwZndMfEsoxA8PgrZ0CcfAFxOhvtYCokyIQZUK2S7QL6jPJrbZUhWJl7c2tzGIliDnGzAv/yfAkBFDKoZw6ctTpLvqDWZLKunHAeljYpNx5isPA9d5ltjwJxLniCTRtbctYIxeKVT94rBqnhEAlzb7/OwT/1xo5/JAkEAw2lJ0J6BzW3rgQ0W7BDeHL3Qcm+LEGJMxCGJ2qEUQPI+n6Z0jMKProKpWtrNj2yJGdURissYf87Z7VU3C3W4Ng=="
    plaintext = RsaUtil.long_decrypt(peo, "WVRcxDI7CsICCcm7eMd377mKTG/t84TUbpZ/a7i71TyfE/fRiggahPhLmwW1QbBWucnSaDdgCBE2mCyC7t2GO9rfgEj1bnbv9nfKcgc3Jhhruhobm/O+DtypZhQmqthNdiZkImm1/wFh/lndCHuNWgjElmysHnJzp7kD3I1KYyxUKL8L2nBc+CDwGc0oaZ2yoR9spPBmWdxYt15NX9q0UfCpElpJOX9s0PBdrcDOux6tlbCjhzKzyrn5QOGTC9w3SNyK+0hPDGgVFbQA5L19N9TRXugBswUNGEQoEZnhoJrNLDZjdAmxaxgnCSqNG+DXhdfgQ9ihuJkmFkvXEUxorw==")
    print('明文：' + plaintext)