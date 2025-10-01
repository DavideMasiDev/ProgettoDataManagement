
-- CREATE DIMENSIONI

drop table if exists "DWH".bridge_genre;
drop table if exists "DWH".bridge_developer;
drop table if exists "DWH".genre;
drop table if exists "DWH".developer;
drop table if exists "DWH".shop;
drop table if exists "DWH".currency;
drop table if exists "DWH".steam_game;
drop table if exists "DWH".date;
drop table if exists "DWH".player;

create table "DWH".date (
	date_pk bigserial primary key,
	full_date timestamp not null,
	year int not null,
	month int not null,
	day int not null
);

create table "DWH".steam_game (
	steam_game_pk bigserial primary key,
	steam_appid bigint not null,
	game_name text not null,
	type text not null,
	fullgame text,
	release_date_pk int not null references "DWH".date ("date_pk")  -- PK to date
);

create table "DWH".genre (
	genre_pk bigserial primary key,
	genre_name text not null
);

create table "DWH".developer (
	developer_pk bigserial primary key,
	developer_name text not null
);

create table "DWH".bridge_genre (
	steam_game_pk bigint not null references "DWH".steam_game ("steam_game_pk"),
	genre_pk bigint not null references "DWH".genre ("genre_pk")
);

create table "DWH".bridge_developer (
	steam_game_pk bigint not null references "DWH".steam_game ("steam_game_pk"),
	developer_pk bigint not null references "DWH".developer ("developer_pk")
);

create table "DWH".shop (
	shop_pk bigserial primary key,
	shop_name text not null
);

create table "DWH".currency (
	currency_pk bigserial primary key,
	currency_name text not null,
	currency_code char(3) not null
);

create table "DWH".player (
	player_pk bigserial primary key,
	player_steamid bigint not null,
	region text not null
);

-- CREATE FATTI


