drop table if exists users;
create table users (
id integer primary key autoincrement,
email text not null,
site_to_parse text not null,
password text not null
);
