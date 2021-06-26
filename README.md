# Covid19_deskApp
<<<<<<< HEAD

PyQtWebEngine 임포트 에러 뜨면 pip install PyQtWebEngine 



sql 구문:
create database covid19;
use covid19;
create table covid19(no int(6), infecD date, place varchar(50), trv varchar(50), infecP varchar(50), state varchar(50))default character set utf8 collate utf8_general_ci;
select * from covid19;


astrazeneca(아스트라제네카) table query: 

create table astrazeneca(
inc_total int(20),
first_inc int(15),
second_inc int(15),
adv_total int(15),
adv_general int(20),
adv_ser_total int(10),
adv_dead int(10),
adv_anap int(7),
adv_major int(10))default charset utf8 collate utf8_general_ci;

아스트라제네카 인서트 쿼리

insert into astrazeneca values(8686025, 797439, 71162, 35667, 34268, 1399, 85, 223, 1091); 


pfizer(화이자) 테이블 쿼리

create table pfizer(
inc_total int(20),
first_inc int(15),
second_inc int(15),
adv_total int(15),
adv_general int(20),
adv_ser_total int(10),
adv_dead int(10),
adv_anap int(7),
adv_major int(10))default charset utf8 collate utf8_general_ci;

화이자 인서트 쿼리

insert into pfizer values(4974697, 3261043, 1713654, 10129, 9179, 950, 153, 72, 725);


얀센 테이블 쿼리

create table janssen(
inc_total int(10),
adv_total int(10),
adv_general int(5),
adv_ser_total int(5),
adv_dead int(5),
adv_anap int(5),
adv_major int(5))default charset utf8 collate utf8_general_ci;

얀센 인서트 쿼리

insert into janssen values(566847, 455, 423, 32, 0, 21, 11);

얀센은 1차접종밖에 안해서 필드가 적음

inc_total은 접체 접종자
first_inc는 1차접종자
second_inc는 2차접종자
adv_total은 전체이상반응
adv_general은 일반이상반응
adv_ser_total은 중대이상반응 전체
adv_dead는 사망자
adv_anap는 아나필랍시스 의심
adv_major은 주요 의심반응


pdf도 올렸으니 pdf보면서 데이터 이해하시길

=======
소프트웨어 공-모-전
>>>>>>> 84c7d8e6b82e197abe983b3b10fef8760cc72b1c
