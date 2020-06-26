-- Selecionar tudo
select distinct 
    hashtag, username, comment, data, timestamp
from raw_hashtag_comments;

-- Selecionar usuario sem geolocalizacao
select distinct rhc.username 
from raw_hashtag_comments as rhc
where rhc.username not in (
	select distinct username from user_geolocation as ug
)
and rhc.username is not null
order by rhc.timestamp asc

-- Remove repetidos
delete from raw_hashtag_comments
where rowid not in (
	select  min(rowid)
    from    raw_hashtag_comments
    group by hashtag, username, comment, data, timestamp
);

-- Selecionar os classificados como positivo
select count(*) 
from raw_hashtag_comments 
where classify = 'positivo';