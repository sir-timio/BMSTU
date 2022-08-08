-- 1. Создать две базы данных на одном экземпляре СУБД SQL Server 2012.
use master
go

if DB_ID('lab13_1') is not null
drop database lab13_1
go
create database lab13_1
go



if DB_ID('lab13_2') is not null
drop database lab13_2
go
create database lab13_2
go

-- 2. создать горизонатльно фрагментированные таблицы

use lab13_1
go

if OBJECT_ID('Patient', 'U') is not null
    drop table Patient
go

create table Patient (
    patient_id int primary key check (patient_id <= 3),
    name nchar(50) NOT NULL,
    surname nchar(50) NOT NULL,
    gender nchar(1) CHECK (gender IN ('M','F')),
    discount int check (discount between 0 and 99) default 0
    );
go

use lab13_2
go

if OBJECT_ID('Patient', 'U') is not null
    drop table Patient
go

create table Patient (
    patient_id int primary key check (patient_id > 3),
    name nchar(50) NOT NULL,
    surname nchar(50) NOT NULL,
    gender nchar(1) CHECK (gender IN ('M','F')),
    discount int check (discount between 0 and 99) default 0
    );
go

-- 3. Создать секционированные представления,
-- обеспечивающие выборку, вставку, изменение, удаление


use lab13_1
go

if OBJECT_ID('PatientView', 'V') is not null
    drop view PatientView;
go

create view PatientView AS
    select * from lab13_1.dbo.Patient
    union all
    select * from lab13_2.dbo.Patient
go

use lab13_2
go

if OBJECT_ID('PatientView', 'V') is not null
    drop view PatientView;
go

create view PatientView AS
    select * from lab13_1.dbo.Patient
    union all
    select * from lab13_2.dbo.Patient
go

insert into PatientView values
    (1, 'Ivan', 'Ivanov', 'M', 10),
    (2, 'Maria', 'Pevchiv', 'F', 20),
    (3, 'Petr', 'Petrov', 'M', 15),
    (4, 'Konstantin', 'Lunev', 'M', 30),
    (5, 'Maria', 'Pevchiv', 'F', 20),
    (6, 'Ivan', 'Shish', 'M', 10)
go

SELECT * FROM PatientView;
go

SELECT * from lab13_1.dbo.Patient;
go
SELECT * from lab13_2.dbo.Patient;
go

DELETE FROM PatientView WHERE name = 'Ivan'
go

SELECT * from lab13_1.dbo.Patient;
go
SELECT * from lab13_2.dbo.Patient;
go

update PatientView
    set discount = 33
    where gender = 'F'

SELECT * from lab13_1.dbo.Patient;
go
SELECT * from lab13_2.dbo.Patient;
go


