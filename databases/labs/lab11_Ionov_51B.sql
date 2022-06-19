use master
go

-- restore database Clinic
-- from disk = '/var/opt/mssql/data/clinic_backup.bak'
-- with replace

use master
go

if DB_ID('Clinic') is not null
    drop database Clinic
go

create database Clinic
on primary (
    name= clinic_dat,
    filename='/var/opt/mssql/data/clinic_dat.mdf',
    size = 10,
    maxsize = 150,
    filegrowth = 15%
)
log on (
    name = clilic_log,
    filename = '/var/opt/mssql/log/clinic_log.ldf',
    size = 5,
    maxsize = 15,
    filegrowth = 15%
    )
go

alter database Clinic
    add filegroup Clinic_FG
go

alter database Clinic
    add file(
        name = clinic_dat1,
        filename = '/var/opt/mssql/data/clinic_dat1.mdf',
        size = 10,
        maxsize = 150,
        filegrowth = 15%
        )
    to filegroup Clinic_FG
go

alter database Clinic
    modify filegroup Clinic_FG default
go

use Clinic
go


if object_id('unique_doctor', 'UQ') is not null
    alter table Doctor drop constraint unique_doctor
go

if object_id('Doctor', 'U') is not null
    drop table Doctor
go

create table Doctor(
    doctor_id int identity(1, 1) primary key,
    mail nvarchar(256) not null,
    name nvarchar(50) not null,
    surname nvarchar(50) not null,
    license_id int not null,
    specialization tinyint not null default 0,
    salary money not null check(salary > 0),
    phone nvarchar(11) not null,
    birth_date smalldatetime not null,
    hire_date smalldatetime not null,
    is_deleted int not null default 0,
    CONSTRAINT unique_doctor UNIQUE (license_id)
)

if object_id('unique_patient', 'UQ') is not null
    alter table Patient drop constraint unique_patient
go

if object_id('Patient', 'U') is not null
    drop table Patient
go

create table Patient(
    patient_id int identity(1, 1) primary key,
    mail nvarchar(256) not null,
    name nvarchar(50) not null,
    surname nvarchar(50) not null,
    phone nvarchar(11) not null,
    birth_date smalldatetime null,
    is_deleted int null default 0,
    constraint unique_patient unique(mail, phone)
)

if object_id('fk_doctor') is not null
    alter table Operation drop constraint fk_doctor
go

if object_id('fk_patient') is not null
    alter table Operation drop constraint fk_patient
go

if object_id('check_duration') is not null
    alter table Operation drop constraint check_duration
go


if object_id('Operation', 'U') is not null
    drop table Operation
go

create table Operation(
    operation_id int identity (1, 1) primary key,
    patient_id int not null,
    doctor_id int not null,
    date date null default (convert(date, getdate())),
    start_time time default (convert(time, getdate())),
    end_time time default (convert(time, getdate())),
    treatment_plan nvarchar(100) default ('consultation'),
    cost_of money not null check (cost_of > 0),
    receipt nvarchar(100) default ('chlorhexidine'),
    constraint fk_doctor foreign key (doctor_id) references Doctor (doctor_id),
    constraint fk_patient foreign key (patient_id) references Patient (patient_id),
    constraint check_duration check (start_time <= end_time)
)
go

if object_id('fk_patient_card') is not null
    alter table Card drop constraint fk_patient_card
go

if object_id('Card', 'U') is not null
    drop table Card
go


create table Card(
    patient_id int primary key not null,
    sex nchar not null check (sex in ('M', 'F')),
    blood_type nchar(3) not null check (blood_type in ('O+', 'A+', 'B+', 'AB+',
                                                       'O-', 'A-', 'B-', 'AB-')),
    allergy nvarchar(100) null default 'none',
    diseases nvarchar(100) null default 'none',
    is_deleted int null default 0,
    constraint fk_patient_card foreign key (patient_id)
        references Patient
)

if object_id('OperationView', 'V') is not null
    drop view OperationView
go

if object_id('dbo.calc_duration', 'FN') is not null
    drop function calc_duration
go

create function dbo.calc_duration(@start_time time, @end_time time)
    returns time
as
    begin
        declare @diff time
        set @diff = convert(varchar(5),
            dateadd(minute, datediff(minute, @start_time, @end_time), 0), 114)
        return @diff
    end
go

select dbo.calc_duration(start_time, end_time) from Operation


if object_id('OperationView', 'V') is not null
    drop view OperationView
go

create view OperationView as
    select p.patient_id, d.doctor_id, o.date,
           o.start_time, dbo.calc_duration(o.start_time, o.end_time) as duration
           from Operation as o
    inner join Doctor as d on o.doctor_id = d.doctor_id
    inner join Patient p on p.patient_id = o.patient_id
go


if object_id('PatientCardIndexView', 'V') is not null
    drop view PatientCardIndexView
go

if exists(select * from sys.indexes where name = 'PatientCardIndex')
    drop index PatientCardIndex on Card
go

create view PatientCardView
with schemabinding
as
    select p.patient_id, c.sex,
           c.blood_type
    from dbo.Card as c
        inner join dbo.Patient P on P.patient_id = c.patient_id
go


create unique clustered index PatientCardIndex
    on PatientCardView(patient_id)
go

-- triggers

-- DOCTOR

if object_id('doctor_update', 'TR') is not null
    drop trigger doctor_update
go

create trigger doctor_update
    on Doctor
    instead of update
    as
    begin
        if update(specialization)
        begin
            RAISERROR('Doctor specialization cannot be updated', 15, 1)
            return
        end
        if update(is_deleted)
        begin
            RAISERROR('Use delete for change is_deleted status', 15, 1)
            return
        end
        if update(birth_date)
            begin
                RAISERROR('Birth date cannot be updated', 15, 1)
                return
            end
        if update(hire_date)
            begin
                RAISERROR('Hire date cannot be updated', 15, 1)
                return
            end
        else
        begin
            update Doctor
            set name = i.name,
                surname = i.surname,
                mail = i.mail,
                license_id = i.license_id,
                salary = i.salary,
                phone = i.phone
            from inserted as i
            where Doctor.doctor_id = i.doctor_id
        end
    end
go

if object_id('doctor_delete', 'TR') is not null
    drop trigger doctor_delete
go

create trigger doctor_delete
    on Doctor
    instead of delete
    as
    begin
        update Doctor
        set is_deleted = 1
        where Doctor.doctor_id in (select doctor_id from deleted)
    end
go

-- Patient

if object_id('patient_update', 'TR') is not null
    drop trigger patient_update
go

create trigger patient_update
    on Patient
    instead of update
    as
    begin
        if update(is_deleted)
        begin
            RAISERROR('Use delete for change is_deleted status', 15, 1)
            return
        end
        if update(birth_date)
            begin
                RAISERROR('Birth date cannot be updated', 15, 1)
                return
            end
        else
        begin
            update Patient
            set name = i.name,
                surname = i.surname,
                mail = i.mail,
                phone = i.phone
            from inserted as i
            where Patient.patient_id = i.patient_id
        end
    end
go


if object_id('patient_delete', 'TR') is not null
    drop trigger patient_delete
go

create trigger patient_delete
    on Patient
    instead of delete
    as
    begin
        select * from deleted

        update Patient
        set is_deleted = 1
        where Patient.patient_id in (select patient_id from deleted)
    end
go


-- CARD

if object_id('card_update', 'TR') is not null
    drop trigger card_update
go

create trigger card_update
    on Card
    instead of update
    as
    begin
        if update(is_deleted)
        begin
            RAISERROR('Use delete for change is_deleted status', 15, 1)
            return
        end
        if update(sex) or update(blood_type)
            begin
                RAISERROR('This params cannot be changed', 15, 1)
                return
            end
        if update(patient_id)
            begin
                RAISERROR('Cannot update patient_id', 15, 1)
                return
            end
        else
        begin
            update Card
            set allergy = i.allergy,
                diseases = i.diseases
            from inserted as i
            where Card.patient_id = i.patient_id
        end
    end
go


if object_id('card_delete', 'TR') is not null
    drop trigger card_delete
go

create trigger card_delete
    on Card
    instead of delete
    as
    begin
        update Card
        set is_deleted = 1
        where Card.patient_id in (select patient_id from deleted)
    end
go

-- OPERATION


if object_id('operation_update', 'TR') is not null
    drop trigger operation_update
go

create trigger operation_update
    on Operation
    instead of update
    as
    begin
        if update(date)
            begin
                RAISERROR('date cannot be updated', 15, 1)
                return
            end
        if update(start_time)
            begin
                RAISERROR('start time cannot be updated', 15, 1)
                return
            end
        if update(cost_of)
            begin
                RAISERROR('cost of operation cannot be modified', 15, 1)
                return
            end
        else
        begin
            update Operation
            set receipt = i.receipt,
                treatment_plan = i.treatment_plan,
                end_time = i.end_time
            from inserted as i
            where Operation.patient_id = i.patient_id
        end
    end
go


if object_id('operation_delete', 'TR') is not null
    drop trigger operation_delete
go

create trigger operation_delete
    on Operation
    instead of delete
    as
    begin
        RAISERROR('cannot delete operation', 15, 1)
        return
    end
go


insert into Patient (mail, name, surname, phone, birth_date) values
('gotrugfn@mail.ru', 'Maria', 'Jhnons', '82856463628', convert(date, '1965-06-18')),
('qjchjqjv@mail.ru', 'Ivan', 'Black', '81617144353', convert(date, '1991-01-16')),
('wejapifz@gmail.ru', 'Arnold', 'Black', '83610476034', convert(date, '1998-07-20')),
('drxausud@yandex.ru', 'Julia', 'Jhnons', '88008626321', convert(date, '1987-01-03')),
('epdptclc@gmail.ru', 'Arnold', 'Smith', '89620896205', convert(date, '1969-11-17'))
go


insert into Card(patient_id, sex, blood_type)
values (1, 'F', 'O+'),
       (2, 'M', 'B-'),
       (3, 'M', 'AB+'),
       (4, 'F', 'A-'),
       (5, 'M', 'A+')
go


insert into Doctor (license_id, specialization, mail, name, surname, phone, birth_date, hire_date, salary) values
(770343, 1, 'hqetsjai@doc.ru', 'Julia', 'Smith', '81498154094', convert(date, '1995-04-17'), convert(date, '2009-10-04'), 150000),
(770392, 2, 'ngelbrav@doc.ru', 'Petr', 'Jhnons', '89756957711', convert(date, '1932-05-22'), convert(date, '2014-07-14'), 100000),
(770425, 3, 'klltnofi@doc.ru', 'Daria', 'Black', '81487390992', convert(date, '1933-05-27'), convert(date, '2013-10-18'), 120000),
(770953, 2, 'xezvtuks@doc.ru', 'Daria', 'Petrenko', '86110158893', convert(date, '1956-03-18'), convert(date, '2012-11-26'), 300000),
(770214, 1, 'rydddoen@doc.ru', 'Paul', 'Black', '87354279621', convert(date, '1952-11-01'), convert(date, '2009-07-22'), 200000)
go


insert into Operation(patient_id, doctor_id, cost_of, date, start_time, end_time)
values
(1, 2, 1000, convert(date, '2020-11-01'), convert(time, '12:00:00'), convert(time, '12:30:00')),
(1, 1, 2000, convert(date, '2020-11-04'), convert(time, '13:00:00'), convert(time, '15:30:00')),
(1, 2, 35000, convert(date, '2020-11-09'), convert(time, '11:20:00'), convert(time, '12:30:00')),
(2, 1, 55000, convert(date, '2020-11-10'), convert(time, '18:00:00'), convert(time, '20:30:00')),
(2, 2, 500, convert(date, '2020-11-15'), convert(time, '12:00:00'), convert(time, '12:30:00'))
go


select * from PatientCardView
go

select * from OperationView
go


select * from Patient
where mail like '%@mail.ru'
go

update Patient
set surname = 'Old'
where birth_date between  convert(date, '1970-01-01') and convert(date, '1990-01-01')
go

select * from Patient
go

delete from Patient
where  name = 'Arnold'
go

select * from Patient
go

select * from Doctor

if object_id('PatientDoctor', 'V') is not null
    drop view PatientDoctor
go

create view PatientDoctor
as
    select p.patient_id, d.doctor_id, d.specialization, o.cost_of
from Operation as o
right join dbo.Doctor d on d.doctor_id = o.doctor_id
left join dbo.Patient p on p.patient_id = o.patient_id
go

select * from PatientDoctor
go

select specialization, count(specialization), avg(cost_of) as avg_cost_of
from PatientDoctor
group by specialization
having avg(cost_of) > 300
order by specialization desc
go




select distinct surname
from Patient
go


select patient_id as id, name, mail from Patient
where patient_id > 3
union select patient_id as id, name, mail from Patient where mail like '%@mail.ru'
except select patient_id as id, name, mail from Patient where name like 'A%'
order by id desc
go



backup database Clinic
to disk = '/var/opt/mssql/data/clinic_backup.bak'
with format,
name = 'Clinic backup'
go"