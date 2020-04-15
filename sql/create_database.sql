/*
This file is used to bootstrap development database.

Note: ONLY development database;
*/

CREATE USER ticket SUPERUSER;
CREATE DATABASE ticket OWNER ticket ENCODING 'utf-8';
