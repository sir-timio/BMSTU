use master;
go

if DB_ID (N'lab8') is not null
	DROP DATABASE lab8;
go

CREATE DATABASE lab8
ON PRIMARY (
	NAME = lab6dat,
	FILENAME = 'C:\DB_labs\lab8dat.mdf',
	SIZE = 10,
	MAXSIZE = UNLIMITED,
	FILEGROWTH = 5
)
go 

use lab8;
go


if OBJECT_ID(N'Tool', N'U') is NOT NULL
	DROP TABLE Tool

CREATE TABLE Tool(
	provider_id int IDENTITY(1,1) PRIMARY KEY,
	provider_name nvarchar(50) DEFAULT N'Stomik',
	name nvarchar(15),
	price int CHECK(price > 0),
	discount int CHECK(discount >= 0 and discount < 100),
	qnt int DEFAULT 0 CHECK(qnt >= 0),
	delivery_days int DEFAULT 0 CHECK(delivery_days > 0),
	box_size int DEFAULT 1 CHECK(box_size in (1, 2, 3, 4, 5))
);

INSERT INTO Tool(price, name, discount, qnt, delivery_days, box_size)
VALUES  (500, N'tweezers',  13, 84, 25, 1),
		(3800, N'scalpel', 34, 79, 20, 1),
		(5900, N'lamp', 12, 47, 12, 5),
		(4800, N'lamp',  25, 58, 1, 5),
		(1200, N'syringe', 40, 89, 4, 2),
		(5500, N'tray',10, 33, 17, 3),
		(2000, N'expander', 7, 53, 3, 3),
		(1600, N'forceps', 30, 43, 16, 1),
		(3500, N'forceps', 34, 69, 13, 2),
		(3000, N'clip',24, 48, 17, 2)
go

if	OBJECT_ID(N'get_delivery_price', N'FN') is NOT NULL
	DROP FUNCTION get_delivery_price
go


if OBJECT_ID(N'select_proc', N'P') is NOT NULL
	DROP PROCEDURE select_proc
go

CREATE PROCEDURE select_proc
		@cursor CURSOR VARYING OUTPUT
AS
		SET @cursor = CURSOR
		SCROLL STATIC FOR
		SELECT price, name, discount, qnt, delivery_days, box_size
		FROM Tool

		OPEN @cursor
go


DECLARE @tool_cursor CURSOR;
EXECUTE select_proc @cursor = @tool_cursor OUTPUT;

FETCH NEXT FROM @tool_cursor;
WHILE (@@FETCH_STATUS = 0)
BEGIN
	FETCH NEXT FROM @tool_cursor;
END

CLOSE @tool_cursor;
DEALLOCATE @tool_cursor;
go

if	OBJECT_ID(N'delivery_calc', N'FN') is NOT NULL
	DROP FUNCTION delivery_calc
go

CREATE FUNCTION delivery_calc(@days int, @box_size int, @discount int)
	RETURNS	int
	WITH EXECUTE AS CALLER
	AS
	BEGIN
		DECLARE @cost int
		DECLARE @new_cost int
		SET @cost = @days * 50 + @box_size * 100
		SET @new_cost = @cost - @cost * CAST((1.0 * @discount / 100) as float)

		RETURN (@new_cost)
	END;
go

if	OBJECT_ID(N'be_in_time', N'FN') is NOT NULL
	DROP FUNCTION be_in_time
go

CREATE FUNCTION be_in_time(@delivery_days int, @operation_days int)
	RETURNS	int
	WITH EXECUTE AS CALLER
	AS
	BEGIN
		DECLARE @res int;
		IF (@delivery_days < @operation_days)
			SET @res = 1
		ElSE
			SET @res = 0

		RETURN @res;
	END;
go

if OBJECT_ID(N'select_add', N'P') IS NOT NULL
	DROP PROCEDURE select_add
go


CREATE PROCEDURE select_add
		@cursor CURSOR VARYING OUTPUT
AS
		SET @cursor = CURSOR
		SCROLL STATIC FOR
		SELECT name, price, discount, delivery_days,
		dbo.delivery_calc(delivery_days, box_size, discount) as delivery_cost
		FROM Tool

		OPEN @cursor
go

DECLARE @tool_cursor CURSOR;
EXECUTE select_add @cursor = @tool_cursor OUTPUT;

FETCH NEXT FROM @tool_cursor;
WHILE (@@FETCH_STATUS = 0)
BEGIN
	FETCH NEXT FROM @tool_cursor;
END

CLOSE @tool_cursor;
DEALLOCATE @tool_cursor;
go

DECLARE @tool_cursor CURSOR;
EXECUTE select_add @cursor = @tool_cursor OUTPUT;
go


if OBJECT_ID(N'dbo.print_proc', N'P') is NOT NULL
		DROP PROCEDURE dbo.print_proc
go

CREATE PROCEDURE dbo.print_proc
AS
	DECLARE @ext_curs CURSOR;

	DECLARE @operation_days int;
	SET @operation_days = 15;
	
	DECLARE @name nvarchar(10);
	DECLARE @price int;
	DECLARE @discount int;
	DECLARE @new_price int;
	DECLARE @qnt int;
	DECLARE @delivery_days int;
	DECLARE @box_size int;
	DECLARE @delivery_cost int;

	EXEC dbo.select_add @cursor = @ext_curs OUTPUT;

	FETCH NEXT FROM @ext_curs INTO @name, @price,  @discount, @delivery_days, @delivery_cost

	WHILE (@@FETCH_STATUS = 0)
	BEGIN
		IF (dbo.be_in_time(@delivery_days, @operation_days) = 1)

			PRINT @name + N' with ' 
			+ CAST(@delivery_days as nvarchar(5)) + N' delivery days ' + 
			N'will be in time for operation in ' + CAST(@operation_days as nvarchar(5)) + N' days'
		ELSE
			PRINT @name + N' with ' 
			+ CAST(@delivery_days as nvarchar(5)) + N' delivery days ' + 
			N'will NOT be in time for operation in ' + CAST(@operation_days as nvarchar(5)) + N' days'

		FETCH NEXT FROM @ext_curs
		INTO @name, @price,  @discount, @delivery_days, @delivery_cost

	END

	CLOSE @ext_curs;
	DEALLOCATE @ext_curs;
go


EXECUTE dbo.print_proc
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
go


ALTER PROCEDURE dbo.print_proc
	@cursor CURSOR VARYING OUTPUT
AS
	SET @cursor = CURSOR 
	FORWARD_ONLY STATIC FOR 
	SELECT * FROM dbo.table_function()
	OPEN @cursor;
go


DECLARE @tool_cursor CURSOR;
EXECUTE dbo.print_proc @cursor = @tool_cursor OUTPUT;

FETCH NEXT FROM @tool_cursor;
WHILE (@@FETCH_STATUS = 0)
	BEGIN
		FETCH NEXT FROM @tool_cursor;
	END

CLOSE @tool_cursor;
DEALLOCATE @tool_cursor;
go

