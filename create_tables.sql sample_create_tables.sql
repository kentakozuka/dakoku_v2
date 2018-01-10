###################
# create database
###################
DROP DATABASE IF EXISTS `sampledb`;
DELETE FROM mysql.user WHERE user='sampleuser';
FLUSH PRIVILEGES;
CREATE DATABASE `sampledb` DEFAULT CHARACTER SET utf8 ;
GRANT ALL ON `sampledb`.* to 'root'@localhost identified by 'root';
FLUSH PRIVILEGES;

###################
# create table
###################
DROP TABLE IF EXISTS USER;
CREATE TABLE QUESTION (
		ID				INT		AUTO_INCREMENT
	,	NAME			INT
	,	SEX 	        VARCHAR(255)
	,	CREATED_DATETIME timestamp not null default current_timestamp
	,	UPDATED_DATETIME timestamp not null default current_timestamp on update current_timestamp
	,	PRIMARY KEY (ID)
	,	INDEX(ID)
) character set utf8mb4;

