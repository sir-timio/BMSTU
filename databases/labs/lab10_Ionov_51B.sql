
first start lab10_create
then use two session for parallel execution of query

=============================
lab10_create.sql
=============================

use master
go

if DB_ID ('lab10') is not null
    DROP DATABASE lab10
go
create database lab10
go

use lab10
go

if OBJECT_ID('patient_payroll') is not null
    drop table patient_payroll
go
create table patient_payroll
(
    id int IDENTITY(1, 1) PRIMARY KEY,
    patient_name varchar(35),
    discount int check (discount between 0 and 99) default 0,
    balance int check(balance >= 0) default 0,
);
go

insert into patient_payroll values
    ('Paul', 10, 1000),
    ('Jul', 15, 1250),
    ('Ivan', 5, 1500),
    ('Petr', 7, 2000),
    ('Ian', 10, 3000)
go
select * from patient_payroll
go

=============================
lab10_1_sess.sql
=============================
-- Лабa 10.
--Режимы выполнения транзакций
--1.Исследовать и проиллюстрировать на примерах
-- различные уровни изоляции транзакций MS SQL Server,
--устанавливаемые с использованием инструкции
-- SET TRANSACTION ISOLATION LEVEL.

--«грязное» чтение(dirty read) – чтение транзакцией записи,
--  измененной другой транзакцией,
--  при этом эти изменения еще не зафиксированы;

--невоспроизводимое чтение(non-repeatable read)
--  при повторном чтении транзакция
--  обнаруживает измененные или удаленные данные,
--  зафиксированные другой завершенной транзакцией; (update/delete)

--–фантомное чтение(phantom read)
--  при повторном чтении транзакция обнаруживает новые строки,
--  вставленные другой завершенной транзакцией; (insert)


-- типы блокировок:
-- S (общий) = сеансу хранения предоставлен общий доступ к ресурсу.
-- X (эксклюзивная) = сеансу с удержанием
--      предоставляется эксклюзивный доступ к ресурсу.
-- IX (с намерением монопольного доступа) = указывает на намерение поместить блокировки X
-- на некоторые подчиненные ресурсы в иерархии блокировок.


--============================================================
--READ UNCOMMITED
-- самый первый уровень изоляции, допускает:
--  грязное чтение (Dirty read)
--  неповторяемое чтение
--  фантомное чтение
--читатели могут считывать
-- данные незваршенной транзакции процесса-писателя
--============================================================

begin transaction
    update dbo.patient_payroll
        set balance = 999
        where id = 1
    waitfor delay '00:00:07'
    rollback transaction
    select * from dbo.patient_payroll
    select resource_type, request_mode from sys.dm_tran_locks
-- commit transaction



--============================================================
--READ COMMITED
--Подтвержденное чтение
--читатели не могут считывать данные незавершенной транзакции,
--но писатели могут изменять уже прочитанные данные.
--Если таблица захвачена, то прочитать данные
--можно только после коммита
-->предотвращает грязное чтение
--============================================================

begin transaction
    select * from dbo.patient_payroll
    update dbo.patient_payroll
        set balance = 888
        where id in (3, 4, 5)
    waitfor delay '00:00:10'
--     rollback transaction
    select * from dbo.patient_payroll
    select resource_type, request_mode from sys.dm_tran_locks
commit transaction





--============================================================
--REPEATABLE READ
--Повторяемое чтение
--повторное чтение данных вернет те же значения,
--что были и в начале транзакции.
--При этом писатели могут вставлять новые записи,
--имеющие статус фантома при незавершенной транзакции.
-->предотвращает невоспроизводимое чтение
--============================================================

begin transaction
    select * from dbo.patient_payroll
        where id in (1, 2)
    waitfor delay '00:00:10'
    select * from dbo.patient_payroll
    where id in (1, 2)
    select * from sys.dm_tran_locks
        --вставка разрешена
        --изменения, затрагивающие данные, выбранные в транзакции, запрещены
        --если данные (строки) не захвачены, их можно менять
    rollback transaction
select * from dbo.patient_payroll




--============================================================
--SERIALIZABLE
--Сериализуемость
--максимальный уровень изоляции,
--гарантирует неизменяемость данных другими процессами
--до завершения транзакции.
-->предотвращает фантомное чтение
--============================================================

begin transaction
    select * from dbo.patient_payroll
        where id in (1,2)
    waitfor delay '00:00:10'
    select * from dbo.patient_payroll
        where id in (1,2)
    select resource_type, request_mode from sys.dm_tran_locks
        --только строки в диапазоне (1 .. 2) PRIMARY KEY будут захвачены
        --остальные строки таблицы можно изменять
    rollback
select * from dbo.patient_payroll




=============================
lab10_2_sess.sql
=============================

use lab10

--READ UNCOMMITED

set transaction isolation level
    read uncommitted
select * from dbo.patient_payroll


--READ COMMITED

set transaction isolation level
    read committed
select * from dbo.patient_payroll


--REPEATABLE READ

update patient_payroll set balance = 777 where id = 3
insert into patient_payroll values ('Kirill', 15, 1000)



--SERIALIZABLE
set transaction isolation level
    serializable
update patient_payroll
set balance = 888 where id = 2