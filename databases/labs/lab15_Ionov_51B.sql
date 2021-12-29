use master
go

if DB_ID('lab15_1') is not null
drop database lab15_1
go

create database lab15_1
go

if DB_ID('lab15_2') is not null
drop database lab15_2
go

create database lab15_2
go

-- 1.Создать в базах данных пункта 1 задания 13 связанные таблицы

use lab15_1
go

if OBJECT_ID('Card', 'U') is not null
drop table Card
go

create table Card (
    card_id int,
    gender nchar(1) check (gender in ('M', 'F')),
    is_deleted int null default 0,
    primary key (card_id)
)

use lab15_2
go

if OBJECT_ID('Patient', 'U') is not null
drop table Patient
go

create table Patient (
    name nchar(50) not null,
    surname nchar(50) not null,
    phone nchar(11) not null,
    card_id int not null unique,
    primary key (phone)
    );
go

use lab15_1
go

-- 2. Создать представления, триггеры
-- обеспечивающие выборку, вставку, изменение, удаление

-- if OBJECT_ID('PatientView', 'V') is not null
-- drop view PatientView
-- go
--
-- create view PatientView as
--     select p.phone, p.name, p.surname,
--            c.card_id, c.gender, c.is_deleted
--     from lab15_2.dbo.Patient p,
--          lab15_1.dbo.Card c
--     where p.card_id = c.card_id
-- go
--
-- select * from PatientView
-- go

--==============
--  INSERT CARD
-- =============
use lab15_1
go

if OBJECT_ID('insert_card_trigger', 'TR') is not null
    drop trigger insert_card_trigger
go
create trigger insert_card_trigger
    on Card
    instead of insert
    as
    begin
        insert into Card(card_id, gender)
        select i.card_id, i.gender from inserted as i
    end
go

--==============
--  INSERT PATIENT
-- =============

use lab15_2
go

if OBJECT_ID('insert_patient_trigger', 'TR') is not null
    drop trigger insert_patient_trigger
go

create trigger insert_patient_trigger
    on Patient
    instead of insert
    as
    begin
        if exists(select p.phone from Patient as p, inserted as i
        where i.phone = p.phone)
        begin
            RAISERROR('cannot add patient with not unique phone', 15, 1)
        end
        else
            begin
                insert into Patient
                select * from inserted
            end
    end
go

use lab15_1
go

insert into Card(card_id, gender)
values
       (1, 'F'),
       (2, 'M'),
       (3, 'F'),
       (4, 'M'),
       (5, 'F')
go

select * from Card
go

use lab15_2
go

insert into Patient(card_id, name, surname, phone)
values
       (1, 'Maria', 'Teresa', '84659209061'),
       (2, 'Oscar', 'Wylde', '83046259525'),
       (3, 'Annushka', 'Butter', '84153262129'),
       (4, 'Jhon', 'Smith', '81366333447'),
       (5, 'Alexa', 'Google', '82263353447')
go

--==============
--  UPDATE CARD
-- =============

use lab15_1
go

if OBJECT_ID('update_card_trigger', 'TR') is not null
    drop trigger update_card_trigger
go

create trigger update_card_trigger
    on Card
    instead of update
    as
    begin
        if update(gender)
        begin
            RAISERROR('gender cannot be modified', 15, 1)
        end
        if update(card_id)
        begin
            RAISERROR('card id cannot be modified', 15, 1)
        end
        if update(is_deleted)
        begin
            update Card
            set Card.is_deleted = i.is_deleted
            from inserted as i
        end
    end
go

-- update Card
-- set gender = 'F'
-- where card_id = 1
-- go

use lab15_2
go

if OBJECT_ID('update_patient_trigger', 'TR') is not null
    drop trigger update_patient_trigger
go

create trigger update_patient_trigger
    on Patient
    instead of update
    as
    begin
        if update(card_id)
        begin
            RAISERROR('card id cannot be modified', 15, 1)
        end
        if update(phone)
        begin
            update Patient
            set phone = i.phone
            from inserted as i
            where Patient.card_id = i.card_id
        end
        if update(name)
        begin
            update Patient
            set name = (select name from inserted)
            where Patient.card_id = (select Patient.card_id from inserted)
        end
        if update(surname)
        begin
            update Patient
            set surname = (select surname from inserted)
            where Patient.card_id = (select Patient.card_id from inserted)
        end
    end
go
select * from Patient

update Patient
set phone = '88888888888'
where card_id = 2
go

use lab15_1
go


--==============
--  DELETE
-- =============
use lab15_1
go

if OBJECT_ID('delete_card_trigger', 'TR') is not null
    drop trigger delete_card_trigger
go

create trigger delete_card_trigger
    on Card
    instead of delete
    as
    begin
        update Card
        set Card.is_deleted = 1
        where Card.card_id in (select card_id from deleted)
        if exists(select card_id from lab15_2.dbo.Patient
            where card_id in (select card_id from deleted))
        begin
            delete from lab15_2.dbo.Patient
            where card_id in (select card_id from deleted) ;
        end
    end
go

use lab15_2
go

if OBJECT_ID('delete_patient_trigger', 'TR') is not null
    drop trigger delete_patient_trigger
go

create trigger delete_patient_trigger
    on Patient
    instead of delete
    as
    begin
        delete from lab15_1.dbo.Card
        where lab15_1.dbo.Card.card_id in (select card_id from deleted) and
              lab15_1.dbo.Card.is_deleted = 0
    end
go

delete
from Patient
where card_id in (1, 2)
go

select * from Patient
go

use lab15_1
go

select * from Card
go
