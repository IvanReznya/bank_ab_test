import pandas as pd
from scipy.stats import chi2_contingency, ttest_ind
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns



# Проверка баланса эксперементальных групп по категориальному признаку
# H0: категориальный признак не зависит от эксперементальной группы
# H1: категориальный признак зависит от эксперементальной группы

ROOT = Path(__file__).resolve().parents[1]
city = pd.read_csv(ROOT / 'data'  / 'processed' / 'city.csv')
device =  pd.read_csv(ROOT / 'data'  / 'processed' / 'device.csv')
age =  pd.read_csv(ROOT / 'data'  / 'processed' / 'age.csv')

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


images_dir = ROOT / 'images'
images_dir.mkdir(exist_ok = True)# CITY
plt.figure(figsize=(9, 5))

sns.barplot(
    data=city,
    x='city',
    y='users_percent',
    hue='experiment_group'
)

plt.xlabel('Город')
plt.ylabel('Доля пользователей, %')
plt.title('Распределение пользователей по городам')
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(images_dir / 'balance_city.png', dpi=300, bbox_inches='tight')
plt.close()


# DEVICE
plt.figure(figsize=(8, 5))

sns.barplot(
    data=device,
    x='device',
    y='users_percent',
    hue='experiment_group'
)

plt.xlabel('Устройство')
plt.ylabel('Доля пользователей, %')
plt.title('Распределение пользователей по устройствам')
plt.tight_layout()

plt.savefig(images_dir / 'balance_device.png', dpi=300, bbox_inches='tight')
plt.close()


# AGE
plt.figure(figsize=(8, 5))

sns.histplot(
    data=age,
    x='age',
    hue='experiment_group',
    stat='density',
    common_norm=False,
    bins=25,
    alpha=0.4
)

plt.xlabel('Возраст')
plt.ylabel('Плотность')
plt.title('Распределение возраста в группах A и B')
plt.tight_layout()

plt.savefig(images_dir / 'balance_age.png', dpi=300, bbox_inches='tight')
