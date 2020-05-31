-- Selecionar tudo
select distinct 
    hashtag, username, comment, data, timestamp
from raw_hashtag_comments;

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