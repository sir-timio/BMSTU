use lab6;
go

-- 1
if OBJECT_ID(N'PatientView', N'V') is NOT NULL
	DROP VIEW PatientView
go


CREATE VIEW PatientView AS
	SELECT *
	FROM Patient
	WHERE date_of_birth BETWEEN (CONVERT(date, N'1930')) AND (CONVERT(date, N'2010'))
go


SELECT * FROM PatientView
go


-- 2
if OBJECT_ID(N'PatientVisitView',N'V') is NOT NULL
	DROP VIEW PatientVisitView;
go

CREATE VIEW PatientVisitView AS
	SELECT p.name,p.gender,p.date_of_birth,
		   v.visit_date,v.visit_time,v.receipt
	FROM Patient as p INNER JOIN Visit as v ON p.patient_id = v.visit_patient
go

SELECT * FROM PatientVisitView
go

-- 3
if EXISTS (SELECT name FROM sys.indexes 
		   WHERE name = N'OperationIndex')  
    DROP INDEX OperationIndex ON Operation;  
go

CREATE INDEX OperationIndex 
		ON Operation (cost_of)
		INCLUDE (patient_name);
go

SELECT cost_of, patient_name  FROM Operation
go

SELECT *  FROM Operation
where cost_of > 100


-- 4
if OBJECT_ID(N'PatientView', N'V') is NOT NULL
	DROP VIEW PatientView
go

if OBJECT_ID(N'PatientIndexView',N'V') is NOT NULL
	DROP VIEW PatientIndexView;
go


if EXISTS (SELECT name FROM sys.indexes  
		   WHERE name = N'PatientVisitIndex')  
    DROP INDEX PatientVisitIndex ON Patient;  
go

CREATE VIEW PatientIndexView 
WITH SCHEMABINDING 
AS
	SELECT name, surname, gender
	FROM dbo.Patient
	WHERE gender = N'W';
go


CREATE UNIQUE CLUSTERED INDEX PatientGender
	on PatientIndexView (name, surname, gender)

SELECT * FROM PatientIndexView
go

SELECT * 
FROM sys.indexes 
WHERE name='PatientIndexView' AND object_id = OBJECT_ID('Patient')
go


if OBJECT_ID(N'table_function',N'TF') is NOT NULL
	DROP FUNCTION table_function
go

CREATE FUNCTION table_function()
	RETURNS @res TABLE(
		name nvarchar(15),
		price int CHECK(price > 0),
		discount int CHECK(discount >= 0 and discount < 100),
		delivery_days int DEFAULT 0 CHECK(delivery_days > 0),
		delivery_cost int
	)
AS
BEGIN
	INSERT @res
	SELECT name, price, discount, delivery_days,
		dbo.delivery_calc(delivery_days, box_size, discount) as delivery_cost
	FROM Tool
	WHERE (dbo.be_in_time(delivery_days, 15) = 1)
	RETURN
END;
