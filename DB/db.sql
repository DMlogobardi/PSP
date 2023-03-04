DROP DATABASE IF EXISTS PSP;
CREATE DATABASE IF NOT EXISTS PSP CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
USE PSP;

DROP TABLE IF EXISTS People;
CREATE TABLE IF NOT EXISTS People(
    IdPeople INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(50) NOT NULL,
    Surname VARCHAR(50) NOT NULL,
    Class VARCHAR(3),
    CF CHAR(16) UNIQUE NOT NULL,
    Sex CHAR(1) NOT NULL DEFAULT 'm',
    Email VARCHAR(100) UNIQUE NOT NULL,
    birthday DATE NOT NULL,
    Sub VARCHAR(24)
);

DROP TABLE IF EXISTS Phones;
CREATE TABLE IF NOT EXISTS Phones(
	IdPhones INT PRIMARY KEY AUTO_INCREMENT,
    number VARCHAR(15) NOT NULL,
    prefix VARCHAR(5) NOT NULL,
    IdPeople INT UNIQUE NOT NULL,
    FOREIGN KEY(IdPeople) REFERENCES People(IdPeople) 
);

DROP TABLE IF EXISTS Vehicles;
CREATE TABLE IF NOT EXISTS Vehicles(
    IdV INT PRIMARY KEY AUTO_INCREMENT,
    Type VARCHAR(8) NOT NULL,
    Plate VARCHAR(8) UNIQUE NOT NULL,
    Owner VARCHAR(70) NOT NULL,
    IdPeople INT NOT NULL,
    FOREIGN KEY(IdPeople) REFERENCES People(IdPeople) 
);

DROP TABLE IF EXISTS Account;
CREATE TABLE IF NOT EXISTS Account(
    IdAccount  INT PRIMARY KEY AUTO_INCREMENT,
    Nick VARCHAR(24) UNIQUE NOT NULL,
    Pass CHAR(128) NOT NULL,
    GK CHAR(4) UNIQUE NOT NULL,
    Ruolo VARCHAR(12) NOT NULL,
    DataReg DATE NOT NULL,
    DataExp DATE,
    IdPeople INT UNIQUE,
    FOREIGN KEY(IdPeople) REFERENCES People(IdPeople) 
);

INSERT INTO Account(Nick, Pass, GK, Ruolo, DataReg) VALUES 
    ('Admin', SHA2('admin', 512), '0000', 'Admin', CURRENT_DATE);

DROP TABLE IF EXISTS Entries;
CREATE TABLE IF NOT EXISTS Entries(
    IdIng INT PRIMARY KEY AUTO_INCREMENT,
    DataIn DATETIME NOT NULL,
    DataOut DATETIME,
    IdAccount INT NOT NULL,
    FOREIGN KEY(IdAccount) REFERENCES Account(IdAccount)
);
