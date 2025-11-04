
-- CREATE DIMENSIONI

drop table if exists "DATAMART".bridge_genre;
drop table if exists "DATAMART".bridge_developer;
drop table if exists "DATAMART".genre;
drop table if exists "DATAMART".developer;
drop table if exists "DATAMART".shop;
drop table if exists "DATAMART".currency;
drop table if exists "DATAMART".steam_game;
drop table if exists "DATAMART"."date";
drop table if exists "DATAMART".player;

create table "DATAMART"."date" (
	date_pk bigserial primary key,
	full_date timestamp not null,
	year int not null,
	month int not null,
	day int not null,
	day_of_week int,
	day_name text,
	month_name text
);

create table "DATAMART".steam_game (
	steam_game_pk bigserial primary key,
	steam_appid bigint not null,
	game_name text not null,
	type text not null,
	fullgame bigint,
	release_date_pk int not null references "DATAMART".date ("date_pk")  -- PK to date
);

create table "DATAMART".genre (
	genre_pk bigserial primary key,
	genre_name text not null
);

create table "DATAMART".developer (
	developer_pk bigserial primary key,
	developer_name text not null
);

create table "DATAMART".bridge_genre (
	steam_game_pk bigint not null references "DWH".steam_game ("steam_game_pk"),
	genre_pk bigint not null references "DWH".genre ("genre_pk"),
	dat_ini_val date not null,
	dat_fin_val date not null
);

create table "DATAMART".bridge_developer (
	steam_game_pk bigint not null references "DWH".steam_game ("steam_game_pk"),
	developer_pk bigint not null references "DWH".developer ("developer_pk"),
	dat_ini_val date not null,
	dat_fin_val date not null
);

create table "DATAMART".shop (
	shop_pk bigserial primary key,
	shop_name text not null
);

create table "DATAMART".currency (
	currency_pk bigserial primary key,
	currency_name text not null,
	currency_code char(3) not null
);

create table "DATAMART".player (
	player_pk bigserial primary key,
	player_steamid bigint not null,
	region text not null,
	country_code varchar(2) not null
);

-- CREATE FATTI

drop table if exists "DATAMART".deal_fact;
drop table if exists "DATAMART".game_statistics_fact;
drop table if exists "DATAMART".player_region_fact;

-- variazioni di prezzo e sconti di un gioco Steam

create table "DATAMART".deal_fact (
	deal_fact_pk bigserial primary key,
	deal_date_pk bigint not null,
	steam_game_pk bigint not null,
	currency_pk bigint not null,
	shop_pk bigint not null,
	regular_price numeric not null,
	deal numeric not null,
	price numeric not null
);

-- popolarità/qualità + distribuzione geografica di un gioco Steam

create table "DATAMART".game_statistics_fact (
	game_statistics_fact_pk bigserial primary key,
	steam_game_pk bigint not null,
	estimated_revenue numeric,
	average_forever numeric,
	total_positive_reviews numeric,
	total_negative_reviews numeric,
	estimated_wishlists numeric,
	dat_ini_val date not null,
	dat_fin_val date not null
);


create table "DATAMART".player_region_fact (
	player_region_pk bigserial primary key,
	player_pk bigint not null,
	steam_game_pk bigint not null,
	dat_ini_val date not null,
	dat_fin_val date not null
);


