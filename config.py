DB_CONFIG = {
    'server': 'LAPTOP-I39GJ4LV\\SQLEXPRESS',  # hoặc địa chỉ IP server
    'database': 'DormitoryDB',
    'username': 'sa',  # Thay bằng username của bạn
    'password': '171205',  # Thay bằng password của bạn
    'driver': '{ODBC Driver 17 for SQL Server}'
}

# Cấu hình ứng dụng
APP_CONFIG = {
    'app_name': 'Quản lý Ký túc xá',
    'version': '1.0.0',
    'window_size': '1200x700',
    'icon_path': 'assets/images/logo.png'
}

# Cấu hình bảo mật
SECURITY_CONFIG = {
    'hash_algorithm': 'sha256',
    'salt': 'dormitory_2024'
}

# Cấu hình giá dịch vụ mặc định
DEFAULT_PRICES = {
    'electricity': 3000,  # VNĐ/kWh
    'water': 15000,       # VNĐ/m³
    'internet': 100000,   # VNĐ/tháng
    'cleaning': 50000,    # VNĐ/tháng
    'deposit': 500000     # VNĐ
}