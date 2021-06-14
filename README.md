# Covid19_deskApp

sql 구문:
create database covid19;
use covid19;
create table covid19(no int(6), infecD date, place varchar(50), trv varchar(50), infecP varchar(50), state varchar(50))default character set utf8 collate utf8_general_ci;
select * from covid19;