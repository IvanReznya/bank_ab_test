import pandas as pd
from scipy.stats import chi2_contingency


# Проверка баланса эксперементальных групп
# H0: категориальный признак не зависит от эксперементальной группы
# H1: категориальный признак зависит от эксперементальной группы

city = pd.read_csv('/Users/ivan/Desktop/bank_project/data/city.csv')
device = pd.read_csv('/Users/ivan/Desktop/bank_project/data/device.csv')

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
