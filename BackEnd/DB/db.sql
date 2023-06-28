DROP DATABASE IF EXISTS PSP;
CREATE DATABASE IF NOT EXISTS PSP CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
USE PSP;

DROP TABLE IF EXISTS People;
CREATE TABLE IF NOT EXISTS People(
    idPeople INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    cF CHAR(16) UNIQUE NOT NULL,
    gender CHAR(1) NOT NULL DEFAULT 'm',
    email VARCHAR(100) UNIQUE NOT NULL,
    birthday DATE NOT NULL,
    sub VARCHAR(24),
    idClass INT REFERENCES Classm(IdClass)
);

DROP TABLE IF EXISTS Classm;
CREATE TABLE IF NOT EXISTS Classm(
    idClass INT PRIMARY KEY AUTO_INCREMENT,
    carrel VARCHAR(2) NOT NULL,
    year INT NOT NULL,
    articulation VARCHAR(30) NOT NULL,
    active VARCHAR(3) DEFAULT "YES" NOT NULL
);

INSERT INTO `classm` (`idClass`, `carrel`, `year`, `articulation`, `active`) VALUES 
(NULL, 'A', '1', 'Elettronica', 'YES'),
(NULL, 'A', '2', 'Elettronica', 'YES'),
(NULL, 'A', '3', 'Elettronica', 'YES'),
(NULL, 'A', '4', 'Elettronica', 'YES'),
(NULL, 'A', '5', 'Elettronica', 'YES'),
(NULL, 'B', '1', 'Elettronica', 'YES'),
(NULL, 'B', '2', 'Elettronica', 'YES'),
(NULL, 'B', '3', 'Elettronica', 'YES'),
(NULL, 'B', '4', 'Elettronica', 'YES'),
(NULL, 'B', '5', 'Elettronica', 'YES'),
(NULL, 'C','1', 'Elettronica', 'YES'),
(NULL, 'C','2', 'Elettronica', 'YES'),
(NULL, 'C','3', 'Elettronica', 'YES'),
(NULL, 'C', '4', 'Elettronica', 'NO'),
(NULL, 'C','5', 'Elettronica', 'YES'),
(NULL, 'D', '1', 'informatica', 'YES'),
(NULL, 'D', '2', 'informatica', 'YES'),
(NULL, 'D', '3', 'informatica', 'YES'),
(NULL, 'D', '4', 'informatica', 'YES'),
(NULL, 'D', '5', 'informatica', 'YES'),
(NULL, 'E', '1', 'informatica', 'YES'),
(NULL, 'E', '2', 'informatica', 'YES'),
(NULL, 'E', '3', 'informatica', 'YES'),
(NULL, 'E', '4', 'informatica', 'YES'),
(NULL, 'E', '5', 'informatica', 'YES'),
(NULL, 'F', '1', 'informatica', 'YES'),
(NULL, 'F', '2', 'informatica', 'YES'),
(NULL, 'F', '3', 'informatica', 'NO'),
(NULL, 'F', '4', 'informatica', 'YES'),
(NULL, 'F', '5', 'informatica', 'YES'),
(NULL, 'G', '1', 'Telecomunicazioni', 'YES'),
(NULL, 'G', '2', 'Telecomunicazioni', 'YES'),
(NULL, 'G', '3', 'Telecomunicazioni', 'YES'),
(NULL, 'G', '4', 'Telecomunicazioni', 'YES'),
(NULL, 'G', '5', 'Telecomunicazioni', 'YES'),
(NULL, 'H', '1', 'Meccanica', 'YES'),
(NULL, 'H', '2', 'Meccanica', 'YES'),
(NULL, 'H', '3', 'Meccanica', 'YES'),
(NULL, 'H', '4', 'Meccanica', 'YES'),
(NULL, 'H', '5', 'Meccanica', 'YES'),
(NULL, 'I', '1', 'Meccanica', 'YES'),
(NULL, 'I', '2', 'Meccanica', 'YES'),
(NULL, 'I', '3', 'Meccanica', 'YES'),
(NULL, 'I', '4', 'Meccanica', 'YES'),
(NULL, 'I', '5', 'Meccanica', 'YES'),
(NULL, 'L', '1', 'Grafica', 'YES'),
(NULL, 'L', '2', 'Grafica', 'YES'),
(NULL, 'L', '3', 'Grafica', 'YES'),
(NULL, 'L', '4', 'Grafica', 'NO'),
(NULL, 'L', '5', 'Grafica', 'NO'),
(NULL, 'M', '1', 'Meccanica', 'NO'),
(NULL, 'M', '2', 'Meccanica', 'YES'),
(NULL, 'M', '3', 'Meccanica', 'YES'),
(NULL, 'M', '4', 'Meccanica', 'YES'),
(NULL, 'M', '5', 'Meccanica', 'YES'),
(NULL, 'N', '1', 'Elettronica', 'YES'),
(NULL, 'N', '2', 'Elettronica', 'YES'),
(NULL, 'N', '3', 'Elettronica', 'YES'),
(NULL, 'N', '4', 'Elettronica', 'NO'),
(NULL, 'N', '5', 'Elettronica', 'NO');




DROP TABLE IF EXISTS Phones;
CREATE TABLE IF NOT EXISTS Phones(
	idPhones INT PRIMARY KEY AUTO_INCREMENT,
    number VARCHAR(15) NOT NULL UNIQUE,
    prefix VARCHAR(5) NOT NULL,
    idPeople INT NOT NULL REFERENCES People(IdPeople) 
);

DROP TABLE IF EXISTS Vehicles;
CREATE TABLE IF NOT EXISTS Vehicles(
    idV INT PRIMARY KEY AUTO_INCREMENT,
    type VARCHAR(8) NOT NULL,
    plate VARCHAR(8) UNIQUE NOT NULL,
    owner VARCHAR(70) NOT NULL,
    idPeople INT NOT NULL REFERENCES People(IdPeople) 
);

DROP TABLE IF EXISTS Account;
CREATE TABLE IF NOT EXISTS Account(
    idAccount  INT PRIMARY KEY AUTO_INCREMENT,
    nick VARCHAR(24) UNIQUE NOT NULL,
    p_ass CHAR(128) NOT NULL,
    gK CHAR(40) UNIQUE NOT NULL,
    ruolo VARCHAR(12) NOT NULL,
    dataReg DATE NOT NULL,
    dataExp DATE,
    valid CHAR(1) DEFAULT 'F', 
    idPeople INT UNIQUE REFERENCES People(IdPeople) 
);

INSERT INTO Account(nick, p_ass, gK, ruolo, dataReg, valid) VALUES 
    ('Admin', SHA2('admin', 256), '0000', 'Admin', CURRENT_DATE, 'O');

DROP TABLE IF EXISTS Entries;
CREATE TABLE IF NOT EXISTS Entries(
    idIng INT PRIMARY KEY AUTO_INCREMENT,
    dataIn DATETIME NOT NULL,
    dataOut DATETIME,
    idAccount INT NOT NULL REFERENCES Account(IdAccount)
);
