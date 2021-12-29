use master
if DB_ID('lab9') is not null
    drop database lab9
go

create database lab9
go

use lab9
go

if OBJECT_ID(N'FK_Patient',N'F') IS NOT NULL
	ALTER TABLE Visit DROP CONSTRAINT FK_Patient
go

if OBJECT_ID(N'Patient',N'U') is NOT NULL
	DROP TABLE Patient;
go

CREATE TABLE Patient (
	patient_id int IDENTITY(1,1) PRIMARY KEY,
	cart_id int DEFAULT 100,
	name nchar(50) DEFAULT 'Petr',
	surname nchar(50) DEFAULT 'Petrov',
	gender nchar(1) CHECK (gender IN ('M','W', 'H', 'D')),
	date_of_birth date NULL,
	discount int DEFAULT 0,
	isDeleted bit DEFAULT 0,
	);
go

SET IDENTITY_INSERT Patient ON
INSERT INTO Patient(patient_id,name,surname, gender, date_of_birth, discount)
VALUES (1,N'Nil', N'Armstrong',N'H', (CONVERT(date, N'1930-02-03')), 10),
	   (2,N'Katy',N'Parry',N'W', (CONVERT(date, N'1984-04-10')), 30),
	   (3,N'Kanye', N'West',N'M', (CONVERT(date, N'1977-11-23')), 15),
	   (4,N'Lana', N'Rey',N'H', (CONVERT(date, N'1985-03-05')), 20),
	   (5,N'Jana', N'Dark',N'W', (CONVERT(date, N'1412-02-12')), 10),
	   (111, N'Dummy',N'DUMMY', N'D', (CONVERT(date, N'2000-05-03')), 5),
       (6,N'DDKaty',N'Parry',N'W', (CONVERT(date, N'1984-04-10')), 30),
	   (7,N'DDDKanye', N'West',N'M', (CONVERT(date, N'1977-11-23')), 15),
	   (8,N'DDLana', N'Rey',N'H', (CONVERT(date, N'1985-03-05')), 20)
SET IDENTITY_INSERT Patient OFF
go


if OBJECT_ID(N'FK_Doctor',N'F') IS NOT NULL
	ALTER TABLE Visit DROP CONSTRAINT FK_Doctor

if OBJECT_ID(N'Doctor',N'U') is NOT NULL
	DROP TABLE Doctor;
go

CREATE TABLE Doctor (
	doctor_id int IDENTITY(1,1) PRIMARY KEY,
	name nchar(50)  NULL,
	surname nchar(50)  NULL,
	date_of_birth date NULL
	);
go

SET IDENTITY_INSERT Doctor ON
INSERT INTO Doctor(doctor_id,name,surname, date_of_birth)
VALUES (1, N'Ivan', N'Ivanov', (CONVERT(date, N'1930-02-03'))),
	   (2, N'Piter', N'Ivanov',  (CONVERT(date, N'1984-04-10'))),
	   (3, N'Ivan', N'Ivanov', (CONVERT(date, N'1977-11-23'))),
	   (4, N'Piter', N'Petrov', (CONVERT(date, N'1985-03-05'))),
	   (5, N'Ivan', N'Petrov', (CONVERT(date, N'1412-02-12'))),
	   (111, N'Dummy',N'DUMMY', (CONVERT(date, N'2000-05-03')))
SET IDENTITY_INSERT Doctor OFF
go



-- 1 Для одной из таблиц пункта 2 лабы 7 создать триггеры
-- на вставку, удаление и добавление
-- при выполнении условий один из триггеров должен иницировать
-- ошибку RAISERROR/THROW
if OBJECT_ID('patient_insert_trigger', 'TR') is not null
    drop trigger patient_insert_trigger
go

create trigger patient_insert_trigger
    on Patient
    for insert
    as
        if exists(
            select *
            from inserted
            where inserted.discount >= 100)
            RAISERROR('The patient has absolute discount', 12, 1)
            WITH LOG;
go


SET IDENTITY_INSERT Patient ON;
insert into Patient (patient_id, discount)
    values (11, 200);
SET IDENTITY_INSERT Patient OFF;
go

if OBJECT_ID('patient_delete_trigger', 'TR') is not null
    drop trigger patient_delete_trigger
go

create trigger patient_delete_trigger
    on Patient
    instead of delete
    as
        begin
            update Patient
            set isDeleted = 1
            where patient_id
            in (select  patient_id from deleted)
        end
go

delete from Patient where patient_id between 5 and 25
go

select * from Patient
go


if OBJECT_ID('patient_update_trigger') is not null
    drop trigger patient_update_trigger
go

create trigger patient_update_trigger
    on Patient
    after update
    as
        print 'table has been updated'
go

update Patient
set discount = 0
where gender = 'H'
go

select * from Patient
go

disable trigger patient_insert_trigger on Patient
go
disable trigger patient_update_trigger on Patient
go
disable trigger patient_delete_trigger on Patient
go

if OBJECT_ID(N'Visit',N'U') is NOT NULL
	DROP TABLE Visit;
go

CREATE TABLE Visit (
	visit_id int IDENTITY(1,1) PRIMARY KEY,
	visit_date date DEFAULT (CONVERT(date,GETDATE())),
	visit_time time(0) DEFAULT (CONVERT(time,GETDATE())),
	patient_id int DEFAULT 111,
	doctor int DEFAULT 111,
	receipt nchar(100) DEFAULT (N'chlorhexidine twice a day'),
	cost_of smallmoney DEFAULT 1000,
	CONSTRAINT FK_Doctor FOREIGN KEY (doctor) REFERENCES Doctor (doctor_id)
    ON DELETE SET DEFAULT,
	CONSTRAINT FK_Patient FOREIGN KEY (patient_id) REFERENCES Patient (patient_id)
	ON DELETE SET DEFAULT
	);
go

INSERT INTO Visit(visit_date,visit_time,patient_id, doctor)
VALUES (CONVERT(date,N'11/01/2021', 103),CONVERT(time,N'12:20:00', 108),1, 5),
	   (CONVERT(date,N'21/06/2021', 103),CONVERT(time,N'15:00:00', 108),2, 4),
	   (CONVERT(date,N'06/10/2014', 103),CONVERT(time,N'17:20:00', 108), 3, 3),
	   (CONVERT(date,N'06/02/2013', 103),CONVERT(time,N'13:15:00', 108), 4, 2),
	   (CONVERT(date,N'08/11/2011', 103),CONVERT(time,N'12:45:00', 108), 5, 1)
go


if OBJECT_ID(N'VisitView',N'V') is NOT NULL
	DROP VIEW VisitView;
go

CREATE VIEW VisitView AS
	SELECT p.name,p.date_of_birth,
		   v.visit_date,v.visit_time,v.receipt
	FROM Patient as p
	    INNER JOIN Visit as v ON p.patient_id = v.patient_id
go

SELECT * FROM VisitView
go

if OBJECT_ID('view_insert_trigger', 'TR') is not null
    drop trigger view_insert_trigger
go

create trigger view_insert_trigger
    on VisitView
    instead of insert
    as
        begin
            set nocount on;
            insert into Patient(name, date_of_birth)
            select distinct i.name, i.date_of_birth
            from inserted i
            where i.name not in (select name from Patient)

            insert into Visit(visit_date, visit_time, receipt, patient_id)
            select i.visit_date, i.visit_time, i.receipt,
                   (select patient_id from Patient as p where i.name = p.name)
            from inserted i

        end
go

insert into VisitView (name, date_of_birth, visit_date,
                       visit_time, receipt) values
 ('Paul', CONVERT(date,N'21/06/2021', 103), CONVERT(date,N'21/06/2021', 103),
     CONVERT(time,N'15:00:00', 108), 'nothing')

go


select * from VisitView
go


select * from Patient
go

if OBJECT_ID('view_delete_trigger', 'TR') is not null
    drop trigger view_delete_trigger
go

create trigger view_delete_trigger
    on VisitView
    instead of delete
    as
        begin
            delete from Patient
            where Patient.name in (select d.name
                from deleted d)
            print'deleted'
        end
go

delete from VisitView
    where name = 'Paul'
go

select * from VisitView
go


if OBJECT_ID('view_update_trigger', 'TR') is not null
    drop trigger view_update_trigger
go

create trigger view_update_trigger
    on VisitView
    instead of update
    as
        begin
            if update(visit_time) or update(visit_date)
                RAISERROR('Visit time cannot be modified', 15, 1)
                WITH LOG
            if update(date_of_birth)
                RAISERROR('Date of birth cannot be modified', 15, 1)
                WITH LOG
            if update(receipt)
                update Visit
                    set receipt = (select receipt
                                        from inserted i
                                        where i.visit_time =  Visit.visit_time
                                        and i.visit_date = Visit.visit_date)
        end
go

update VisitView
    set visit_date = CONVERT(date,N'21/06/2021', 103)
    where receipt = 'nothing'

select * from Visit
go
