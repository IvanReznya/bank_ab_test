select 
e.experiment_group,
t.category,
count(*) as count_transactions,
coalesce(round(sum(t.amount_rub)::numeric, 2),0) as total_amount,
coalesce(round(sum(t.bank_revenue_rub)::numeric, 2),0) as total_revenue
from transactions t 
left join experiment e on t.user_id  = e.user_id 
group by e.experiment_group, t.category
order by e.experiment_group, t.category
