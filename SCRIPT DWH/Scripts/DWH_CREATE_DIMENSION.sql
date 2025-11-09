
-- CREATE DIMENSIONI

drop table if exists "DWH".bridge_genre;
drop table if exists "DWH".bridge_developer;
drop table if exists "DWH".genre cascade;
drop table if exists "DWH".developer cascade;
drop table if exists "DWH".shop;
drop table if exists "DWH".currency;
drop table if exists "DWH".steam_game cascade;
drop table if exists "DWH"."date";
drop table if exists "DWH".player;

create table "DWH"."date" (
	date_pk bigserial primary key,
	full_date timestamp not null,
	year int not null,
	month int not null,
	day int not null,
	day_of_week int,
	day_name text,
	month_name text
);

create table "DWH".steam_game (
	steam_game_pk bigserial primary key,
	steam_appid bigint not null,
	game_name text not null,
	type text not null,
	fullgame bigint,
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
	genre_pk bigint not null references "DWH".genre ("genre_pk"),
	dat_ini_val date not null,
	dat_fin_val date not null
);

create table "DWH".bridge_developer (
	steam_game_pk bigint not null references "DWH".steam_game ("steam_game_pk"),
	developer_pk bigint not null references "DWH".developer ("developer_pk"),
	dat_ini_val date not null,
	dat_fin_val date not null
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
	region text not null,
	country_code varchar(2) not null
);

-- CREATE FATTI

drop table if exists "DWH".deal_fact;
drop table if exists "DWH".game_statistics_fact;
drop table if exists "DWH".player_region_fact;

-- variazioni di prezzo e sconti di un gioco Steam

create table "DWH".deal_fact (
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

create table "DWH".game_statistics_fact (
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


create table "DWH".player_region_fact (
	player_region_pk bigserial primary key,
	player_pk bigint not null,
	steam_game_pk bigint not null,
	dat_ini_val date not null,
	dat_fin_val date not null
);


