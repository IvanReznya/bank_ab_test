select 
e.experiment_group,
u.age
from experiment e 
left join users u on e.user_id = u.user_id 
where u.age is not null
order by e.experiment_group , u.age 
