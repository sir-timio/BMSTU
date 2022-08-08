use master
go

if DB_ID('lab14_1') is not null
drop database lab14_1
go

create database lab14_1
go

if DB_ID('lab14_2') is not null
drop database lab14_2
go

create database lab14_2
go

-- 1.Создать в базах данных пункта 1 задания 13 таблицы, содержащие вертикально фрагментированные данные.

use lab14_1
go

if OBJECT_ID('Patient', 'U') is not null
drop table Patient
go

create table Patient (
    patient_id int not null,
    name nchar(50) NOT NULL,
    -- surname nchar(50) NOT NULL,
    -- gender nchar(1) CHECK (gender IN ('M','F')),
    discount int check (discount between 0 and 99) default 0,
    is_deleted int null default 0
    primary key (patient_id)
    );
go


use lab14_2
go

if OBJECT_ID('Patient', 'U') is not null
drop table Patient
go

create table Patient (
    patient_id int not null,
    -- name nchar(50) NOT NULL,
    surname nchar(50) NOT NULL,
    gender nchar(1) CHECK (gender IN ('M','F')) not null,
    -- discount int check (discount between 0 and 99) default 0,
    -- is_deleted int not null default 0,
    primary key (patient_id)
    );
go

-- 2. Создать представления, триггеры
-- обеспечивающие выборку, вставку, изменение, удаление

if OBJECT_ID('PatientView', 'V') is not null
drop view PatientView
go

create view PatientView as
    select P1.patient_id,
           P1.name, P2.surname,
           P2.gender, P1.discount,
           P1.is_deleted
    from lab14_1.dbo.Patient P1,
         lab14_2.dbo.Patient P2
    where P1.patient_id = P2.patient_id
go

select * from PatientView

if object_id('insert_trigger') is not null
    drop trigger insert_trigger
go

--==============
--  INSERT
-- =============
create trigger insert_trigger
    on PatientView
    instead of insert
    as
    begin
        set nocount on;
        select * from inserted
        if exists(select discount from inserted where discount > 30)
            begin
                print 'WoW such a big discount there!'
            end
        insert into lab14_1.dbo.Patient(patient_id, name, discount)
        select patient_id, name, discount from inserted
        insert into lab14_2.dbo.Patient(patient_id, surname, gender)
        select  patient_id, surname, gender from inserted
    end
go

insert into PatientView(patient_id, name, surname, gender, discount) values
    (1, 'Ivan', 'Ivanov', 'M', 10),
    (2, 'Masha', 'Kirsanova', 'F', 15),
    (3, 'Savel', 'Wild', 'M', 40),
    (4, 'Katerina', 'Kabanova', 'F', 20)
go

select * from PatientView
go

--==============
--  UPDATE
-- =============

if OBJECT_ID('update_trigger') is not null
    drop trigger update_trigger
go

create trigger update_trigger
    on PatientView
    instead of update
    as
    begin
        if update(gender)
        begin
            RAISERROR('gender cannot be modified in RUSSIA', 15, 1)
        end
        else if update(patient_id)
            begin
                RAISERROR('ID cannot be modified!', 15, 1)
            end
        else
            begin
                update lab14_1.dbo.Patient
                set Patient.name = i.name ,Patient.discount = i.discount
                from inserted as i
                where Patient.patient_id = i.patient_id

                update lab14_2.dbo.Patient
                set Patient.surname = i.surname, Patient.gender = i.gender
                from inserted as i
                where Patient.patient_id = i.patient_id
            end
    end
go

update PatientView
set discount = 33
where gender = 'F'
go

select * from PatientView
go

--==============
--  DELETE
-- =============
if OBJECT_ID('delete_trigger', 'TR') is not null
    drop trigger delete_trigger
go

create trigger delete_trigger
    on PatientView
    instead of delete
    as
    begin
        update lab14_1.dbo.Patient
        set Patient.is_deleted = 1
        where Patient.patient_id = (select patient_id from deleted)
    end
go

delete
from PatientView
where discount < 15
go

select * from PatientView
go
