use master;
go

if DB_ID (N'lab6') is not null
	DROP DATABASE lab6;
go

CREATE DATABASE lab6
ON PRIMARY (
	NAME = lab6dat,
	FILENAME = 'C:\DB_labs\lab6dat.mdf',
	SIZE = 10,
	MAXSIZE = UNLIMITED,
	FILEGROWTH = 5
)
go 

use lab6;
go 


if OBJECT_ID(N'FK_Patient',N'F') IS NOT NULL
	ALTER TABLE Visit DROP CONSTRAINT FK_Patient

if OBJECT_ID(N'Patient',N'U') is NOT NULL
	DROP TABLE Patient;
go

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
	   (N'Nicola',N'Tesla',30, 30),
	   (N'Maykl', N'Jeksos', 10, 10),
	   (N'Peter', N'Jackson', 12, 11)

go

SELECT * FROM Patient
go
print ('q1: ' + cast(IDENT_CURRENT('dbo.Patient') as nvarchar(3)))
print ('q1(scope): ' + cast(SCOPE_IDENTITY() as nvarchar(3)))

if OBJECT_ID(N'Operation',N'U') is NOT NULL
	DROP TABLE Operation;
go


CREATE TABLE Operation (
	operation_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT (NEWID()),
	doctor_name nchar(50) NOT NULL,
	patient_name nchar(50) NOT NULL,
	cost_of smallmoney NULL CHECK (cost_of > 0),
	);
go

INSERT INTO Operation(doctor_name,patient_name,cost_of)
OUTPUT inserted.operation_id
VALUES (N'Who', N'Cat', 2000),
	   (N'Strange', N'Cat', 3000),
	   (N'Aibolit', N'Rabbit', 1000), 
	   (N'Aibolit', N'Cat', 1000),
	   (N'Aibolit', N'Dog', 1000),
	   (N'Aibolit', N'Bird', 1000)



go


SELECT * FROM Operation
go


if OBJECT_ID(N'FK_Patient',N'F') IS NOT NULL
	ALTER TABLE Visit DROP CONSTRAINT FK_Patient
go

if OBJECT_ID(N'Patient',N'U') is NOT NULL
	DROP TABLE Patient;
go

CREATE TABLE Patient (
	patient_id int DEFAULT 10,
	number_patient_card int DEFAULT 100,
	name nchar(50) NOT NULL,
	surname nchar(50) NOT NULL,
	gender nchar(1) CHECK (gender IN (N'M',N'W', N'H')),
	date_of_birth date NULL
	PRIMARY KEY (patient_id)
	);
go


INSERT INTO Patient(patient_id,name,surname, gender, date_of_birth)
VALUES (1,N'Nil', N'Armstong',N'H', (CONVERT(date, N'1930-02-03'))),
	   (2,N'Katy',N'Parry',N'W', (CONVERT(date, N'1984-04-10'))),
	   (3,N'Kanye', N'West',N'M', (CONVERT(date, N'1977-11-23'))),
	   (4,N'Lana', N'Rey',N'H', (CONVERT(date, N'1985-03-05'))),
	   (5,N'Jana', N'Dark',N'W', (CONVERT(date, N'1412-02-12'))),
	   (10, N'Dummy',N'DUMMY', N'W', (CONVERT(date, N'2000-05-03')))
go

SELECT * FROM Patient
go


if OBJECT_ID(N'FK_Doctor',N'F') IS NOT NULL
	ALTER TABLE Visit DROP CONSTRAINT FK_Doctor
go

if OBJECT_ID(N'Doctor',N'U') is NOT NULL
	DROP TABLE Doctor;
go

CREATE TABLE Doctor (
	doctor_id int DEFAULT 10,
	name nchar(50) NOT NULL,
	surname nchar(50) NOT NULL,
	date_of_birth date NULL
	PRIMARY KEY (doctor_id)
	);
go

INSERT INTO Doctor(doctor_id,name,surname, date_of_birth)
VALUES (1, N'Ivan', N'Ivanov', (CONVERT(date, N'1930-02-03'))),
	   (2, N'Piter', N'Ivanov',  (CONVERT(date, N'1984-04-10'))),
	   (3, N'Ivan', N'Ivanov', (CONVERT(date, N'1977-11-23'))),
	   (4, N'Piter', N'Petrov', (CONVERT(date, N'1985-03-05'))),
	   (5, N'Ivan', N'Petrov', (CONVERT(date, N'1412-02-12'))),
	   (10, N'Dummy',N'DUMMY', (CONVERT(date, N'2000-05-03')))
go

SELECT * FROM Doctor
go



if OBJECT_ID(N'Visit',N'U') is NOT NULL
	DROP TABLE Visit;
go


CREATE TABLE Visit (
	visit_id int IDENTITY(1,1) PRIMARY KEY,
	visit_date date DEFAULT (CONVERT(date,GETDATE())),
	visit_time time(0) DEFAULT (CONVERT(time,GETDATE())),
	visit_patient int DEFAULT 10,
	doctor int REFERENCES Doctor (doctor_id),
	receipt nchar(100) DEFAULT (N'chlorhexidine twice a day'),
	cost_of smallmoney DEFAULT 1000,
	CONSTRAINT FK_Patient FOREIGN KEY (visit_patient) REFERENCES Patient (patient_id)
	ON DELETE SET DEFAULT
	);
go

INSERT INTO Visit(visit_date,visit_time,visit_patient, doctor)
VALUES (CONVERT(date,N'11-01-2021'),CONVERT(time,N'12:20:00'),1, 5),
	   (CONVERT(date,N'21-06-2021'),CONVERT(time,N'15:00:00'),2, 4),
	   (CONVERT(date,N'06-10-2014'),CONVERT(time,N'17:20:00'), 3, 3),
	   (CONVERT(date,N'06-02-2013'),CONVERT(time,N'13:15:00'), 4, 2),
	   (CONVERT(date,N'08-11-2011'),CONVERT(time,N'12:45:00'), 5, 1)


go

SELECT * FROM Visit
go

DELETE FROM Patient
	WHERE gender = N'H'
go 

SELECT * FROM Patient
go
SELECT * FROM Visit
go
