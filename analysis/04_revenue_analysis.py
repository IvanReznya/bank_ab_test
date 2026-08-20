import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

user_metrics = pd.read_csv('/Users/ivan/Desktop/bank_project/data/user_metrics.csv')

alpha = 0.05

A = user_metrics[user_metrics['experiment_group'] == 'A']['sum_revenue']
B = user_metrics[user_metrics['experiment_group'] == 'B']['sum_revenue']

# 1. Описательная статистика

print('-' * 60)
print(user_metrics.groupby('experiment_group')['sum_revenue'].describe())

# 2. Welch t-test
# H0: mean_A = mean_B
# H1: mean_A != mean_B

t_stat, p_value = ttest_ind(A, B, equal_var = False)

mean_A = np.mean(A)
mean_B = np.mean(B)

difference = mean_B - mean_A
uplift = difference / mean_A * 100

print('-' * 60)
print(f'mean_A = {mean_A:.3f}')
print(f'mean_B = {mean_B:.3f}')
print(f'difference = {difference:.3f}')
print(f'uplift = {uplift:.2f}%')
print(f't = {t_stat:.2f}')
print(f'p_value = {p_value:.6f}')

if p_value < alpha:
    print('Отвергаем H0.')
    print('Различие статистически значимо.')
else:
    print('Нет оснований отвергать H0.')
    print('Статистически значимого различия не обнаружено.')
print('-' * 60)

# 3. Bootstrap 95% доверительный интервал

rng = np.random.default_rng(42)

N = 10000
bootstrap_diff = []

A_np = A.to_numpy()
B_np = B.to_numpy()

for _ in range(N):
    boot_A = rng.choice(A_np, size = len(A_np), replace = True)
    boot_B = rng.choice(B_np, size = len(B_np), replace = True)
    bootstrap_diff.append(np.mean(boot_B) - np.mean(boot_A))

lower = np.percentile(bootstrap_diff, 2.5)
upper = np.percentile(bootstrap_diff, 97.5)
print(f'95% bootstrap CI = [{lower:.2f}, {upper:.2f}]')
print('-' * 60)

# 4. Revenue среди пользователей с положительным доходом

positive = user_metrics[user_metrics['sum_revenue'] > 0]

A_positive = positive[positive['experiment_group'] == 'A']['sum_revenue']
B_positive = positive[positive['experiment_group'] == 'B']['sum_revenue']

t_stat_positive, p_value_positive = ttest_ind(A_positive, B_positive, equal_var = False)

mean_A_positive = np.mean(A_positive)
mean_B_positive = np.mean(B_positive)

print('Revenue среди пользователей с положительным доходом')
print('-' * 60)
print(f'mean_A = {mean_A_positive:.3f}')
print(f'mean_B= {mean_B_positive:.3f}')
print(f't = {t_stat_positive:.2f}')
print(f'p_value = {p_value_positive:.6f}')

if p_value_positive < alpha:
    print('Различие статистически значимо.')
else:
    print('Статистически значимого различия не обнаружено.')
print('-' * 60)



