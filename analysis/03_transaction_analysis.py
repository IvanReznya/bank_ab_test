import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

user_metrics = pd.read_csv('/Users/ivan/Desktop/bank_project/data/user_metrics.csv')

alpha = 0.05

A = user_metrics[user_metrics['experiment_group'] == 'A']['count_transactions']
B = user_metrics[user_metrics['experiment_group'] == 'B']['count_transactions']

# 1. Описательная статистика

print('-' * 60)
print(user_metrics.groupby('experiment_group')['count_transactions'].describe())

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
    print('Статистического значимого различия не обнаружено.')
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

