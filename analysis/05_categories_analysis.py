import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Анализ транзакций по категориям
#
# Цель:
# определить, какие категории транзакций вносят наибольший вклад
# в изменение дохода банка между группами A и B.
#
# Анализ является описательным.
# Статистические тесты по отдельным категориям не проводятся

ROOT = Path(__file__).resolve().parents[1]
categories = pd.read_csv(ROOT / 'data'  / 'processed' / 'categories.csv')

# 1. Сравнение общего дохода банка по категориям

revenue = categories.pivot(
    index = 'category',
    columns = 'experiment_group',
    values = 'total_revenue'
)

revenue['difference'] = revenue['B'] - revenue['A']
revenue['uplift_%'] = revenue['difference'] / revenue['A'] * 100

# 2. Сравнение количества транзакций по категориям

transactions = categories.pivot(
    index = 'category',
    columns = 'experiment_group',
    values = 'count_transactions'
)

transactions['difference'] = transactions['B'] - transactions['A']
transactions['uplift_%'] = transactions['difference'] / transactions['A'] * 100

# 3. Сравнение среднего дохода банка с одной транзакции

categories['revenue_per_transaction'] = categories['total_revenue'] / categories['count_transactions']
revenue_per_transaction = categories.pivot(
    index = 'category',
    columns = 'experiment_group',
    values = 'revenue_per_transaction'
)

revenue_per_transaction['difference'] = revenue_per_transaction['B'] - revenue_per_transaction['A']
revenue_per_transaction['uplift_%'] = revenue_per_transaction['difference'] / revenue_per_transaction['A'] * 100


print('-' * 60)
print('Total revenue')
print('-' * 60)
print(revenue.sort_values('difference', ascending = False))
print('-' * 60)
print('Count transactions')
print('-' * 60)
print(transactions.sort_values('difference', ascending = False))
print('-' * 60)
print(revenue_per_transaction)
print('-' * 60)

images_dir = ROOT / 'images'
images_dir.mkdir(exist_ok = True)

plt.figure(figsize=(10, 5))

sns.barplot(
    data=categories,
    x='category',
    y='total_revenue',
    hue='experiment_group'
)

plt.xlabel('Категория')
plt.ylabel('Total revenue, ₽')
plt.title('Revenue по категориям: A vs B')
plt.xticks(rotation=30)
plt.legend(title='Группа')

plt.tight_layout()

plt.savefig(
    images_dir / 'categories_revenue.png',
    dpi=300,
    bbox_inches='tight'
)

plt.figure(figsize=(10, 5))

sns.barplot(
    data=categories,
    x='category',
    y='total_revenue',
    hue='experiment_group'
)

plt.xlabel('Категория')
plt.ylabel('Total revenue, ₽')
plt.title('Revenue по категориям: A vs B')
plt.xticks(rotation=30)
plt.legend(title='Группа')

plt.tight_layout()

plt.savefig(
    images_dir / 'categories_revenue.png',
    dpi=300,
    bbox_inches='tight'
)

plt.figure(figsize=(10, 5))

sns.pointplot(
    data=categories,
    x='category',
    y='revenue_per_transaction',
    hue='experiment_group',
    dodge=True
)

plt.xlabel('Категория')
plt.ylabel('Revenue на транзакцию, ₽')
plt.title('Revenue на одну транзакцию по категориям')
plt.xticks(rotation=30)
plt.legend(title='Группа')

plt.tight_layout()

plt.savefig(
    images_dir / 'categories_revenue_per_transaction.png',
    dpi=300,
    bbox_inches='tight'
)


