CREATE DATABASE `profile_1`;
USE `profile_1`;
CREATE TABLE `profile` (
      `id` int(11) AUTO_INCREMENT,
      `birth_date` date,
      `first_name` varchar(30),
      `last_name` varchar(30),
      `phone_number1` varchar(30),
      `phone_number2` varchar(30),
      `address_id` int(11) REFERENCES `address`(`id`),
      PRIMARY KEY (`id`)
    );
CREATE TABLE `address` (
      `id`    int(11)  AUTO_INCREMENT,
      `line1` varchar(100) DEFAULT '',
      `street` varchar(100) DEFAULT '',
      `suburb` varchar(100)  DEFAULT '',
      `postcode` varchar(100) DEFAULT '',
      `state` varchar(100) DEFAULT '',
      `country` varchar(100) DEFAULT 'Australia',
      PRIMARY KEY (`id`)
    );

CREATE TABLE `document` (
	`id`	INTEGER AUTO_INCREMENT,
	`doc_type`	varchar(100),
	`document`	LONGBLOB,
	`client_id` int(11) REFERENCES `profile`(`id`),
  PRIMARY KEY (`id`)
);