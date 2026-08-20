import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
user_metrics = pd.read_csv(ROOT / 'data'  / 'processed' / 'user_metrics.csv')


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


# 4. Распределение количества транзакций
images_dir = ROOT / 'images'
images_dir.mkdir(exist_ok = True)


plt.figure(figsize=(8, 5))

sns.histplot(
    data=user_metrics,
    x='count_transactions',
    hue='experiment_group',
    discrete=True,
    stat='density',
    common_norm=False,
    alpha=0.4
)

plt.xlabel('Количество транзакций на пользователя')
plt.ylabel('Плотность')
plt.title('Распределение количества транзакций')

plt.tight_layout()

plt.savefig(
    images_dir / 'transactions_distribution.png',
    dpi=300,
    bbox_inches='tight'
)



plt.figure(figsize=(6, 5))

plt.errorbar(
    x=['B - A'],
    y=[difference],
    yerr=[
        [difference - lower],
        [upper - difference]
    ],
    fmt='o',
    capsize=8
)

plt.axhline(
    y=0,
    linestyle='--'
)

plt.ylabel('Разница среднего количества транзакций')
plt.title('Эффект версии B на количество транзакций')

plt.tight_layout()

plt.savefig(
    images_dir / 'transactions_effect.png',
    dpi=300,
    bbox_inches='tight'
)
