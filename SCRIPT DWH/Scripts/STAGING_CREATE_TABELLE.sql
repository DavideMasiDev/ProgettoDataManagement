drop table if exists "STAGING".raw_data;
drop table if exists "STAGING".released_game;
drop table if exists "STAGING".game_player_region;
drop table if exists "STAGING".price_history;
drop table if exists "STAGING".genre_classification;

create table if not exists "STAGING".raw_data (
	raw_data_pk bigserial primary key,
	steam_appid bigint not null,
	name text not null,
	type varchar(4) not null, 
	fullgame int
);

create table if not exists "STAGING".released_game (
	released_game_pk bigserial primary key,
	name text not null,
	steam_appid bigint not null,
	short_description text,
	required_age varchar(2),
	controller_support bool,
	supported_languages text,
	developers text,
	publishers text,
	platforms text,
	categories text,
	genres text,
	release_date date not null,
	followers text,
	estimated_wishlists text,
	tags text,
	price numeric,
	estimated_revenue text,
	estimated_units text,
	currency text,
	owners text,
	average_forever int,
	average_2weeks int,
	median_forever int,
	median_2weeks int,
	concurrent_users int,
	total_positive int,
	total_negative int,
	total_reviews int
);

create table if not exists "STAGING".game_player_region (
	game_player_region_pk bigserial primary key,
	steam_appid bigint not null,
	player_steamid bigint not null,
	region varchar(50) not null,
	country_code char(2) not null
);

create table if not exists "STAGING".price_history (
	price_history_pk bigserial primary key,
	steam_appid bigint not null,
	name text not null,
	timestamp date not null,
	price numeric not null,
	deal numeric not null,
	regular_price numeric not null,
	currency varchar(3) not null,
	shop text not null
);

create table "STAGING".genre_classification (
	genre_classification_pk bigserial primary key,
	genre_name text not null,
	classification text
)