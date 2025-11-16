drop database course_manager;

create database if not exists course_manager;

use course_manager;

create table if not exists roles(
	Id int primary key auto_increment,
    `Name` varchar(31) not null unique
);

insert into roles(Name) values ('Student'), ('Instructor'), ('Admin');

create table if not exists users(
	Id int primary key auto_increment,
    `Name` varchar(63) not null,
    Email varchar(64) not null unique,
    Role_id int not null,
    foreign key (role_id) references roles(Id)
);

create table if not exists courses(
	Id int primary key auto_increment,
    Title varchar(31) not null unique,
    `Description` varchar(255) not null,
    Instructor_id int not null,
    foreign key (Instructor_id) references users(Id)
);

create table if not exists modules(
	Id int primary key auto_increment,
    Title varchar(31) not null unique,
    Course_id int not null,
    foreign key (Course_id) references courses(Id)
);

create table if not exists lessons(
	Id int primary key auto_increment,
    Title varchar(31) not null unique,
    Module_id int not null,
    foreign key (Module_id) references modules(Id)
);

create table if not exists enrollments(
	Student_id int not null,
    Course_id int not null,
    foreign key (Student_id) references users(Id),
    foreign key (Course_id) references courses(Id),
    primary key (Student_id, Course_id)
);