with users_on_experiment as 
(
select 
e.experiment_group,
count(*) as users
from experiment e 
group by e.experiment_group 
)
,
users_on_applications as 
(
select 
e.experiment_group, 
count(*) as users_application
from applications a 
left join experiment e on a.user_id = e.user_id 
group by e.experiment_group 
)
,
users_on_approved as 
(
select 
e.experiment_group, 
count(*) as users_approved
from applications a 
left join experiment e on a.user_id = e.user_id 
where approved = 1
group by e.experiment_group 
)
,
users_on_activated as 
(
select 
e.experiment_group, 
count(*) as users_activated
from applications a 
left join experiment e on a.user_id = e.user_id 
where a.activated = 1
group by e.experiment_group 
)
select 
users_on_experiment.experiment_group,
users,
users_application,
users_approved,
users_activated,
round(users_application * 100.0 /users, 2) as CR_application,
round(users_approved * 100.0 /users_application, 2) as CR_approved,
round(users_activated * 100.0 /users_approved, 2) as CR_activated,
round(users_activated * 100.0 /users, 2) as CR_total
from users_on_experiment
join users_on_applications on users_on_experiment.experiment_group  = users_on_applications.experiment_group 
join users_on_approved  on users_on_experiment.experiment_group  = users_on_approved.experiment_group 
join users_on_activated on users_on_experiment.experiment_group  = users_on_activated.experiment_group 
