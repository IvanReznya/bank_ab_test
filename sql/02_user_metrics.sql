select
e.experiment_group,
u.user_id,
count(t.user_id ) as count_transactions,
coalesce(round(avg(t.bank_revenue_rub)::numeric, 2), 0) as avg_revenue,
coalesce(round(sum(t.bank_revenue_rub)::numeric, 2), 0) as sum_revenue
from users u
left join transactions t on u.user_id  = t.user_id 
left join experiment e on u.user_id  = e.user_id  
group by e.experiment_group , u.user_id 
order by e.experiment_group
