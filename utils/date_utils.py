from datetime import datetime, timedelta

class DateUtils:
    @staticmethod
    def format_date(date_obj, format='%d/%m/%Y'):
        """Format ngày"""
        if isinstance(date_obj, str):
            return date_obj
        return date_obj.strftime(format) if date_obj else ''
    
    @staticmethod
    def parse_date(date_str, format='%Y-%m-%d'):
        """Parse string thành date"""
        try:
            return datetime.strptime(date_str, format).date()
        except:
            return None
    
    @staticmethod
    def get_current_date():
        """Lấy ngày hiện tại"""
        return datetime.now().date()
    
    @staticmethod
    def get_current_month():
        """Lấy tháng hiện tại (YYYY-MM)"""
        return datetime.now().strftime('%Y-%m')
    
    @staticmethod
    def add_months(date, months):
        """Cộng thêm tháng"""
        return date + timedelta(days=30 * months)
    
    @staticmethod
    def calculate_age(birth_date):
        """Tính tuổi"""
        if isinstance(birth_date, str):
            birth_date = DateUtils.parse_date(birth_date)
        
        today = datetime.now().date()
        age = today.year - birth_date.year
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        return age