import hashlib

class Encryption:
    @staticmethod
    def hash_md5(text):
        """Mã hóa MD5"""
        return hashlib.md5(text.encode()).hexdigest()
    
    @staticmethod
    def hash_sha256(text):
        """Mã hóa SHA256"""
        return hashlib.sha256(text.encode()).hexdigest()
    
    @staticmethod
    def verify_password(plain_password, hashed_password):
        """Kiểm tra mật khẩu"""
        return Encryption.hash_md5(plain_password) == hashed_password