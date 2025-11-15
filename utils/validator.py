import re
from datetime import datetime

class Validator:
    @staticmethod
    def is_empty(value):
        """Kiểm tra rỗng"""
        return not value or value.strip() == ''
    
    @staticmethod
    def is_valid_email(email):
        """Kiểm tra email hợp lệ"""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def is_valid_phone(phone):
        """Kiểm tra số điện thoại hợp lệ"""
        pattern = r'^0\d{9}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def is_valid_date(date_str, format='%Y-%m-%d'):
        """Kiểm tra ngày hợp lệ"""
        try:
            datetime.strptime(date_str, format)
            return True
        except:
            return False
    
    @staticmethod
    def is_number(value):
        """Kiểm tra số"""
        try:
            float(value)
            return True
        except:
            return False
    
    @staticmethod
    def is_positive_number(value):
        """Kiểm tra số dương"""
        try:
            return float(value) > 0
        except:
            return False
    
    @staticmethod
    def validate_student_code(code):
        """Validate MSSV"""
        if Validator.is_empty(code):
            return False, "MSSV không được để trống!"
        if len(code) < 5 or len(code) > 20:
            return False, "MSSV phải từ 5-20 ký tự!"
        return True, ""
    
    @staticmethod
    def validate_full_name(name):
        """Validate họ tên"""
        if Validator.is_empty(name):
            return False, "Họ tên không được để trống!"
        if len(name) < 3:
            return False, "Họ tên phải từ 3 ký tự trở lên!"
        return True, ""
    
    @staticmethod
    def validate_phone(phone):
        """Validate SĐT"""
        if not Validator.is_empty(phone):
            if not Validator.is_valid_phone(phone):
                return False, "Số điện thoại không hợp lệ! (10 số, bắt đầu bằng 0)"
        return True, ""
    
    @staticmethod
    def validate_email(email):
        """Validate email"""
        if not Validator.is_empty(email):
            if not Validator.is_valid_email(email):
                return False, "Email không hợp lệ!"
        return True, ""
    
    @staticmethod
    def validate_id_card(id_card):
        """Validate CMND/CCCD"""
        if Validator.is_empty(id_card):
            return False, "CMND/CCCD không được để trống!"
        if len(id_card) not in [9, 12]:
            return False, "CMND/CCCD phải là 9 hoặc 12 số!"
        if not id_card.isdigit():
            return False, "CMND/CCCD chỉ chứa số!"
        return True, ""