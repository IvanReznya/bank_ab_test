import pandas as pd
from scipy.stats import chi2_contingency, ttest_ind
from pathlib import Path


# Проверка баланса эксперементальных групп по категориальному признаку
# H0: категориальный признак не зависит от эксперементальной группы
# H1: категориальный признак зависит от эксперементальной группы

ROOT = Path(__file__).resolve().parents[1]
city = pd.read_csv(ROOT / 'data' / 'city.csv')
device =  pd.read_csv(ROOT / 'data' / 'device.csv')
age =  pd.read_csv(ROOT / 'data' / 'age.csv')

alpha = 0.05

city_table = city.pivot(
    index = 'experiment_group',
    columns = 'city',
    values = 'users'
)

device_table = device.pivot(
    index = 'experiment_group',
    columns = 'device',
    values = 'users'
)

def chi2_pearson(table, alpha=0.05):
    chi2, p_value, dof, expected = chi2_contingency(table)
    print('-' * 60)
    print(f'chi_2 = {chi2}')
    print(f'p_value = {p_value}')
    print(f'dof = {dof}')
    if p_value < alpha:
        print('Отвеграем H0.')
        print('Обнаружена статистически значимая зависимость.')
    else:
        print('Нет оснований отвергать H0.')
        print('Статистически значимой зависимости не обнаружено.')
    print('-' * 60)

print('City')
chi2_pearson(city_table, alpha)
print('Device')
chi2_pearson(device_table, alpha)

# Проверка баланса эксперементальных групп по количественному признаку (возрасту)
# H0: mu_age_A = mu_age_B
# H1: mu_age_A != mu_age_B

# Используем t-критерий Уэлча

age_A = age[age['experiment_group'] == 'A']['age'].dropna()
age_B = age[age['experiment_group'] == 'B']['age'].dropna()

t_stat, p_value = ttest_ind(
    age_A,
    age_B,
    equal_var = False
)
print('Age')
print('-' * 60)
print(f'Mean A = {age_A.mean():.2f}')
print(f'Mean B = {age_B.mean():.2f}')
print(f'Difference B - A = {age_B.mean() - age_A.mean():.2f}')
print(f't_stat = {t_stat:.2f}')
print(f'p_value = {p_value:.2f}')
if p_value < alpha:
    print('Отвеграем H0.')
    print('Различие между группами статистически значимо.')
else:
    print('Нет оснований отвергать H0.')
    print('Статистического значимого различия не обнаружено.')
print('-' * 60)
