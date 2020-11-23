create database academico_vestibular;

use academico_vestibular;

CREATE TABLE dados (
	id bigint
    cpf varchar(255),
    etnia varchar(255),
    sexo varchar(1),
    escola_origem varchar(255),
	renda_familiar varchar(255),
	estado varchar(255),
    cidade varchar(255),
	data_nascimento varchar(255),
	matr_situacao varchar(255)
);