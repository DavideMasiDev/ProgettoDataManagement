-- TEST PER DASHBOARD 'Reviews Indie'

with game_perc as (
	select gsf.steam_game_pk,
	case
		when (gsf.total_positive_reviews + gsf.total_negative_reviews) >  0 then gsf.total_positive_reviews / (gsf.total_positive_reviews + gsf.total_negative_reviews)
		else -100
	end as perc,
	gsf.total_positive_reviews,
	gsf.total_negative_reviews
	from "DATAMART".game_statistics_fact gsf 
	join "DATAMART".bridge_genre bg on (bg.steam_game_pk = gsf.steam_game_pk)
	join "DATAMART".genre g on (g.genre_pk = bg.genre_pk)
	where g.genre_name = 'Indie'
)
select count(*)
from game_perc
where perc >= 0.6 and perc < 0.7;


with matrice_generi as (
	select distinct least(g1.genre_name, g2.genre_name) as genre_name_1, greatest(g1.genre_name, g2.genre_name) as genre_name_2
	from "DATAMART".genre g1, "DATAMART".genre g2
	where (g1.classification in ('GENRE') or g1.genre_name in ('Tower Defense', 'Roguelike')) and (g2.classification in ('GENRE') or g2.genre_name in ('Tower Defense', 'Roguelike')) and g1.genre_name != g2.genre_name 
	and g1.genre_name != 'Indie' and g2.genre_name != 'Indie'
	and g1.genre_name not in ('2D Fighter', '3D Fighter', '2D Platformer', '3D Platformer', 'Action Roguelike', 'Action RTS', 'Action', 'Adventure', 'Arena Shooter', 'Automobile Sim', 'Beat ''em up', 'Board Game', 'Boomer Shooter', 'Card Battler', 'Character Action Game', 'Chess', 'Classic', 'Colony Sim', 'Combat Racing', 'Escape Room', 'Football (American)', 'Football (Soccer)', 'GameMaker', 'Grand Strategy', 'Hobby Sim', 'Idler', 'Immersive Sim', 'Job Simulator', 'Looter Shooter', 'Mahjong', 'Medical Sim', 'Musou', 'On-Rails Shooter', 'Open World Survival Craft', 'Outbreak Sim', 'Party-Based RPG', 'Political Sim', 'Precision Platformer', 'Psychological Horror', 'Puzzle Platformer', 'Roguelike Deckbuilder', 'Roguevania', 'RPGMaker', 'Runner', 'Sandbox', 'Shoot ''Em Up', 'Solitaire', 'Spectacle fighter', 'Tabletop', 'Tactical', 'Top-Down Shooter', 'Trading', 'Trading Card Game', 'Traditional Roguelike', 'Turn-Based Combat', 'Turn-Based Strategy', 'Turn-Based Tactics', 'Twin Stick Shooter', 'Vehicular Combat', 'Walking Simulator', 'Wargame', 'Word Game', 'Hero Shooter', 'Bullet Hell', 'CRPG', 'Roguelite')
	and g2.genre_name not in ('2D Fighter', '3D Fighter', '2D Platformer', '3D Platformer', 'Action Roguelike', 'Action RTS', 'Action', 'Adventure', 'Arena Shooter', 'Automobile Sim', 'Beat ''em up', 'Board Game', 'Boomer Shooter', 'Card Battler', 'Character Action Game', 'Chess', 'Classic', 'Colony Sim', 'Combat Racing', 'Escape Room', 'Football (American)', 'Football (Soccer)', 'GameMaker', 'Grand Strategy', 'Hobby Sim', 'Idler', 'Immersive Sim', 'Job Simulator', 'Looter Shooter', 'Mahjong', 'Medical Sim', 'Musou', 'On-Rails Shooter', 'Open World Survival Craft', 'Outbreak Sim', 'Party-Based RPG', 'Political Sim', 'Precision Platformer', 'Psychological Horror', 'Puzzle Platformer', 'Roguelike Deckbuilder', 'Roguevania', 'RPGMaker', 'Runner', 'Sandbox', 'Shoot ''Em Up', 'Solitaire', 'Spectacle fighter', 'Tabletop', 'Tactical', 'Top-Down Shooter', 'Trading', 'Trading Card Game', 'Traditional Roguelike', 'Turn-Based Combat', 'Turn-Based Strategy', 'Turn-Based Tactics', 'Twin Stick Shooter', 'Vehicular Combat', 'Walking Simulator', 'Wargame', 'Word Game', 'Hero Shooter', 'Bullet Hell', 'CRPG', 'Roguelite')
),
giochi_indie as (
	select gsf.steam_game_pk
	from "DATAMART".game_statistics_fact gsf 
	join "DATAMART".bridge_genre bg on (bg.steam_game_pk = gsf.steam_game_pk)
	join "DATAMART".genre g on (g.genre_pk = bg.genre_pk)
	where g.genre_name = 'Indie'
),
genre_list as (
	select gsf.steam_game_pk, string_to_array(string_agg(g.genre_name, ','), ',') as genres_list 
	from "DATAMART".game_statistics_fact gsf 
	join "DATAMART".bridge_genre bg on (bg.steam_game_pk = gsf.steam_game_pk)
	join "DATAMART".genre g on (g.genre_pk = bg.genre_pk)
	join giochi_indie gi on (gi.steam_game_pk = gsf.steam_game_pk)
	where g.classification in ('TOP LEVEL GENRE', 'GENRE')
	group by gsf.steam_game_pk
),
numero_di_giochi_indie_per_coppie_di_genere as (
	select mg.genre_name_1, mg.genre_name_2, count(distinct gl.steam_game_pk) as count_giochi_coppie
	from matrice_generi mg
	join genre_list gl on (mg.genre_name_1 = any(gl.genres_list) and mg.genre_name_2 = any(gl.genres_list))
	group by mg.genre_name_1, mg.genre_name_2
),
numero_di_giochi_indie_per_genere as (
	select g.genre_name, count(distinct gsf.steam_game_pk) as count_giochi
	from "DATAMART".game_statistics_fact gsf 
	join "DATAMART".bridge_genre bg on (bg.steam_game_pk = gsf.steam_game_pk)
	join "DATAMART".genre g on (g.genre_pk = bg.genre_pk)
	join giochi_indie gi on (gi.steam_game_pk = gsf.steam_game_pk) -- per calcolare le numeriche inerenti solamente ai giochi Indie
	where g.classification in ('TOP LEVEL GENRE', 'GENRE') and g.genre_name not in ('Indie') -- and gsf.steam_game_pk = 654209 (Test: Disco Elysium)
	group by g.genre_name 
),
numero_di_giochi_distinti_coppie as (
	select genre1.genre_name as genre_name_1, genre1.count_giochi as count_giochi_1, genre2.genre_name as genre_name_2, genre2.count_giochi as count_giochi_2
	from numero_di_giochi_indie_per_genere genre1, numero_di_giochi_indie_per_genere genre2
	where genre1.genre_name != genre2.genre_name
)
select mg.genre_name_1, 
coalesce(x.count_giochi_1, 0) as count_giochi_1, 
mg.genre_name_2, 
coalesce(x.count_giochi_2, 0) as count_giochi_2,  
coalesce(y.count_giochi_coppie, 0) as count_giochi_coppie
from matrice_generi mg
left join numero_di_giochi_distinti_coppie x on (mg.genre_name_1 = x.genre_name_1 and mg.genre_name_2 = x.genre_name_2)
left join numero_di_giochi_indie_per_coppie_di_genere y on (mg.genre_name_1 = y.genre_name_1 and mg.genre_name_2 = y.genre_name_2);
-- 13340

with vista as (
	select max(sg.game_name) as game_name, 
	max(sg."type") as "type",
	max(d.full_date) as release_date,
	string_agg(g.genre_name, ',') as genres,
	max(gsf.total_positive_reviews) as total_positive_reviews,
	max(gsf.total_negative_reviews) as total_negative_reviews,
	max(gsf.total_positive_reviews + gsf.total_negative_reviews) as total_reviews,
	max(gsf.estimated_revenue) as estimated_revenue
	from "DATAMART".game_statistics_fact gsf 
	join "DATAMART".bridge_genre bg on (bg.steam_game_pk = gsf.steam_game_pk)
	join "DATAMART".genre g on (g.genre_pk = bg.genre_pk)
	join "DATAMART".steam_game sg on (sg.steam_game_pk = gsf.steam_game_pk)
	join "DATAMART"."date" d on (d.date_pk = sg.release_date_pk)
	where g.classification in ('TOP LEVEL GENRE', 'GENRE')
	group by gsf.steam_game_pk
)
select game_name,
"type",
release_date,
concat(',', genres, ',') as genres,
total_positive_reviews,
total_negative_reviews,
total_reviews,
estimated_revenue
from vista
where 'Action-Adventure' = any(string_to_array(genres, ',')) and 'Horror' = any(string_to_array(genres, ',')) and 'Indie' = any(string_to_array(genres, ',')) 


