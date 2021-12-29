use master;
go
if DB_ID (N'lab6') is not null
drop database lab6;
go
create database lab6
on primary (
	NAME = lab6dat,
	FILENAME = 'C:\DB_labs\lab6dat.mdf',
	SIZE = 10,
	MAXSIZE = UNLIMITED,
	FILEGROWTH = 5
)
go 

use lab6;
go 


-- ������� ������� � ���������������� ��������� ������.
-- �������� ����, ��� ������� ������������ ����������� (CHECK), �������� �� ��������� (DEFAULT).

CREATE TABLE Patient (
	patient_id int IDENTITY(1,1) PRIMARY KEY,
    name nchar(30) NOT NULL,
	surname nchar(30) NOT NULL,
	discount1 smallint CHECK (discount1 < 100),
	discount2 smallint CHECK (discount2 < 100),
	CONSTRAINT checkSale CHECK (discount1+discount2 < 100)
	);
go

INSERT INTO Patient(name,surname,discount1,discount2)
VALUES (N'Jack',N'Sparrow', 15, 30),
	   (N'Nicola',N'Tesla',30, 30)

go

SELECT * FROM Patient
go
print ('q1: ' + cast(IDENT_CURRENT('dbo.Patient') as nvarchar(3)))
print ('q1(scope): ' + cast(SCOPE_IDENTITY() as nvarchar(3)))

-- �������� ������������� SCOPE_IDENTITY() --
SELECT IDENT_CURRENT('dbo.Patient') as last_id
go

-- ������� ������� � ��������� ������ �� ������ ����������� ����������� ��������������


CREATE TABLE Operation (
	operation_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT (NEWID()),
	doctor_name nchar(50) NOT NULL,
	patient_name nchar(50) NOT NULL,
	cost_of smallmoney NULL CHECK (cost_of > 0),
	);
go

INSERT INTO Operation(doctor_name,patient_name,cost_of)
-- ��� ��������� ������������ ����������� �������������� --
OUTPUT inserted.operation_id
VALUES (N'�������', N'����', 2000),
	   (N'����', N'�����', 3000),
	   (N'�������', N'������� ����', 5000)
go

-- ��� ��������� ������������ ����������� �������������� --

SELECT * FROM Operation
go


-- ������� ������� � ��������� ������ �� ������ ������������������



-- ������� ��� ��������� �������, � �������������� �� ��� ��������� �������� �������� --
-- ��� ����������� ��������� ����������� (NO ACTION| CASCADE | SET NULL | SET DEFAULT). --
if OBJECT_ID(N'FK_Patient',N'F') IS NOT NULL
	ALTER TABLE Visit DROP CONSTRAINT FK_Patient
go

if OBJECT_ID(N'Patient',N'U') is NOT NULL
	DROP TABLE Patient;
go

CREATE TABLE Patient (
	patient_id int DEFAULT 10,
	number_patient_card int NULL,
	name nchar(50) NOT NULL,
	surname nchar(50) NOT NULL,
	gender nchar(1) CHECK (gender IN (N'�',N'�')),
	date_of_birth datetime NULL
	PRIMARY KEY (patient_id)
	);
go

INSERT INTO Patient(patient_id,name,surname, gender)
VALUES (1,N'�����', N'�������',N'�'),
	   (2,N'����',N'������',N'�'),
	   (3,N'����', N'��������',N'�'),
	   (4,N'������', N'�����',N'�')
go

SELECT * FROM Patient
go

if OBJECT_ID(N'Visit',N'U') is NOT NULL
	DROP TABLE Visit;
go

CREATE TABLE Visit (
	visit_id int IDENTITY(1,1) PRIMARY KEY,
	visit_date date DEFAULT (CONVERT(date,GETDATE())),
	visit_time time(0) DEFAULT (CONVERT(time,GETDATE())),
	visit_patient int DEFAULT 10,
	receipt nchar(100) DEFAULT (N'������������ 2 ���� � ����'),
	CONSTRAINT FK_Patient FOREIGN KEY (visit_patient) REFERENCES Patient (patient_id)
	ON DELETE SET DEFAULT
	);
go

INSERT INTO Visit(visit_date,visit_time,visit_patient)
VALUES (CONVERT(date,N'11-01-2021'),CONVERT(time,N'12:20:00'),3),
	   (CONVERT(date,N'21-06-2021'),CONVERT(time,N'15:00:00'),2),
	   (CONVERT(date,N'06-10-2014'),CONVERT(time,N'17:20:00'),1)
go

SELECT * FROM Visit
go

DELETE FROM Patient
	WHERE gender = N'�'
go 

SELECT * FROM Patient
go
SELECT * FROM Visit
go