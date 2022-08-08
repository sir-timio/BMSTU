USE MASTER;
GO

CREATE DATABASE lab5_db
ON PRIMARY
  ( NAME = lab5_dat,
    FILENAME = 'C:\DB_labs\lab5_dat.mdf',
    SIZE = 10,
    MAXSIZE = 50,
    FILEGROWTH = 15% );

USE MASTER;
GO 
IF DB_ID (N'lab5_db') IS NOT NULL
DROP DATABASE lab5_db;

CREATE DATABASE lab5_db
ON PRIMARY
  ( NAME = lab5_dat,
    FILENAME = 'C:\DB_labs\lab5_dat.mdf',
    SIZE = 10,
    MAXSIZE = 50,
    FILEGROWTH = 15% );
GO

USE lab5_db;
GO
CREATE TABLE lab5_table (c1 int, c2 varchar(10))

ALTER DATABASE lab5_db ADD FILEGROUP lab5_fg

ALTER DATABASE lab5_db
ADD FILE (NAME=lab5_db_dat,
	FILENAME = 'C:\DB_labs\dat.mdf', SIZE = 10,
	MAXSIZE = 100, FILEGROWTH = 5)
TO FILEGROUP lab5_fg;
	
ALTER DATABASE lab5_db
MODIFY FILEGROUP lab5_fg DEFAULT;

CREATE TABLE lab5_table2 (c2 int, c3 char(20))


ALTER DATABASE lab5_db
MODIFY FILEGROUP [PRIMARY] DEFAULT;

DROP table lab5_table2;

ALTER DATABASE lab5_db
REMOVE FILE lab5_db_dat;

ALTER DATABASE lab5_db
REMOVE FILEGROUP lab5_fg;
GO

CREATE SCHEMA lab5_sc;
GO

ALTER SCHEMA lab5_sc
    TRANSFER lab5_table;

DROP TABLE lab5_sc.lab5_table;
DROP SCHEMA lab5_sc;
USE master;
DROP DATABASE lab5_db;

--sp_help
