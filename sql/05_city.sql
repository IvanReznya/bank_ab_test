select 
e.experiment_group,
u.city,
count(u.user_id) as users,
round(count(u.user_id) * 100.0 / sum(count(*)) over (partition by e.experiment_group), 2) as users_percent
from experiment e 
left join users u on e.user_id  = u.user_id 
where nullif(trim(u.city), '') is not null
group by e.experiment_group, u.city
order by e.experiment_group, u.city
