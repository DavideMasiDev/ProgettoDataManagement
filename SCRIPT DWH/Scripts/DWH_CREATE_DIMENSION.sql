create table "DWH"."DATE" (
	"DATE_PK" int primary key,
	"FULL_DATE" timestamp not null,
	"YEAR" int not null,
	"MONTH" int not null,
	"DAY" int not null
);

create table "DWH"."STEAM_GAME" (
	"STEAM_GAME_PK" int primary key, -- App ID Steam
	"GAME_NAME" text not null,
	"TYPE" text not null,
	"FULLGAME" text,
	"RELEASE_DATE_PK" int not null references "DWH"."DATE" ("DATE_PK")  -- PK to date
);

create table "DWH"."GENRE" (
	"GENRE_PK" int primary key,
	"GENRE_NAME" text not null
);

create table "DWH"."DEVELOPER" (
	"DEVELOPER_PK" int primary key,
	"DEVELOPER_NAME" text not null
);

create table "DWH"."BRIDGE_GENRE" (
	"STEAM_GAME_PK" int not null,
	"GENRE_PK" int not null
);

create table "DWH"."BRIDGE_DEVELOPER" (
	"STEAM_GAME_PK" int not null,
	"DEVELOPER_PK" int not null
);

create table "DWH"."SHOP" (
	"SHOP_PK" int primary key
	"SHOP_NAME" text not null
);

create table "DWH"."CURRENCY" (
	"CURRECY_PK" int primary key,
	"CURRENCY_NAME" text not null,
	"CURRECY_CODE" char(3) not null,
)

