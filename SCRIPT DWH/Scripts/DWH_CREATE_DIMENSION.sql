create table "DWH".date (
	date_pk int primary key,
	full_date timestamp not null,
	year int not null,
	month int not null,
	day int not null
);

create table "DWH".steam_game (
	steam_game_pk int primary key, -- App ID Steam
	game_name text not null,
	type text not null,
	fullgame text,
	release_date_pk int not null references "DWH".date ("date_pk")  -- PK to date
);

create table "DWH".genre (
	genre_pk int primary key,
	genre_name text not null
);

create table "DWH".developer (
	developer_pk int primary key,
	developer_name text not null
);

create table "DWH".bridge_genre (
	steam_game_pk int not null,
	genre_pk int not null
);

create table "DWH".bridge_developer (
	steam_game_pk int not null,
	"DEVELOPER_PK" int not null
);

create table "DWH".shop (
	shop_pk int primary key
	shop_name text not null
);

create table "DWH".currency (
	currency_pk int primary key,
	currency_name text not null,
	currency_code char(3) not null,
)

