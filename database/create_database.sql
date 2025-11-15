CREATE DATABASE DormitoryDB;
GO

USE DormitoryDB;
GO

-- Bảng Users (Tài khoản đăng nhập)
CREATE TABLE Users (
    UserID INT PRIMARY KEY IDENTITY(1,1),
    Username NVARCHAR(50) UNIQUE NOT NULL,
    Password NVARCHAR(255) NOT NULL,
    FullName NVARCHAR(100) NOT NULL,
    Role NVARCHAR(20) NOT NULL CHECK (Role IN ('Admin', 'Student')),
    CreatedDate DATETIME DEFAULT GETDATE(),
    IsActive BIT DEFAULT 1
);

-- Bảng Students (Sinh viên)
CREATE TABLE Students (
    StudentID INT PRIMARY KEY IDENTITY(1,1),
    StudentCode NVARCHAR(20) UNIQUE NOT NULL,
    FullName NVARCHAR(100) NOT NULL,
    DateOfBirth DATE NOT NULL,
    Gender NVARCHAR(10) CHECK (Gender IN (N'Nam', N'Nữ')),
    PhoneNumber NVARCHAR(15),
    Email NVARCHAR(100),
    IDCard NVARCHAR(20) UNIQUE NOT NULL,
    Address NVARCHAR(255),
    Faculty NVARCHAR(100),
    Major NVARCHAR(100),
    Class NVARCHAR(50),
    Status NVARCHAR(20) DEFAULT N'Đang ở',
    UserID INT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Bảng Rooms (Phòng)
CREATE TABLE Rooms (
    RoomID INT PRIMARY KEY IDENTITY(1,1),
    RoomNumber NVARCHAR(10) UNIQUE NOT NULL,
    Building NVARCHAR(10) NOT NULL,
    Floor INT NOT NULL,
    RoomType NVARCHAR(20) NOT NULL,
    Capacity INT NOT NULL,
    CurrentOccupancy INT DEFAULT 0,
    PricePerMonth DECIMAL(10,0) NOT NULL,
    Status NVARCHAR(20) DEFAULT N'Trống',
    Description NVARCHAR(255)
);

-- Bảng Contracts (Hợp đồng)
CREATE TABLE Contracts (
    ContractID INT PRIMARY KEY IDENTITY(1,1),
    StudentID INT NOT NULL,
    RoomID INT NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    MonthlyFee DECIMAL(10,0) NOT NULL,
    Deposit DECIMAL(10,0) NOT NULL,
    Status NVARCHAR(20) DEFAULT N'Đang hiệu lực',
    SignedDate DATE DEFAULT GETDATE(),
    Notes NVARCHAR(255),
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID)
);

-- Bảng Invoices (Hóa đơn)
CREATE TABLE Invoices (
    InvoiceID INT PRIMARY KEY IDENTITY(1,1),
    ContractID INT NOT NULL,
    StudentID INT NOT NULL,
    BillingMonth NVARCHAR(7) NOT NULL,
    RoomFee DECIMAL(10,0) NOT NULL,
    ElectricityFee DECIMAL(10,0) DEFAULT 0,
    WaterFee DECIMAL(10,0) DEFAULT 0,
    InternetFee DECIMAL(10,0) DEFAULT 0,
    ServiceFee DECIMAL(10,0) DEFAULT 0,
    TotalAmount DECIMAL(10,0) NOT NULL,
    PaidAmount DECIMAL(10,0) DEFAULT 0,
    RemainingAmount DECIMAL(10,0) NOT NULL,
    Status NVARCHAR(20) DEFAULT N'Chưa thanh toán',
    DueDate DATE,
    PaymentDate DATE,
    CreatedDate DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (ContractID) REFERENCES Contracts(ContractID),
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
);

-- Bảng Payments (Lịch sử thanh toán)
CREATE TABLE Payments (
    PaymentID INT PRIMARY KEY IDENTITY(1,1),
    InvoiceID INT NOT NULL,
    Amount DECIMAL(10,0) NOT NULL,
    PaymentMethod NVARCHAR(50),
    PaymentDate DATETIME DEFAULT GETDATE(),
    Notes NVARCHAR(255),
    FOREIGN KEY (InvoiceID) REFERENCES Invoices(InvoiceID)
);

-- Index để tăng tốc truy vấn
CREATE INDEX idx_student_code ON Students(StudentCode);
CREATE INDEX idx_room_number ON Rooms(RoomNumber);
CREATE INDEX idx_invoice_month ON Invoices(BillingMonth);
CREATE INDEX idx_contract_student ON Contracts(StudentID);

GO