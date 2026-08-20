import pandas as pd
from statsmodels.stats.proportion import proportions_ztest, confint_proportions_2indep

# Анализ воронки
# H0: p_A = p_B
# H1: p_A != p_B


funnel = pd.read_csv('/Users/ivan/Desktop/bank_project/data/funnel.csv')

# Уровень значимости

alpha = 0.05

# Поправка Бонферрони для трех вторичных метрик: alpha_corrected = alpha/3.

alpha_corrected = alpha / 3

def ztest_with_ci(count, nobs, alpha=0.05):
    z_stat, p_value = proportions_ztest(count, nobs, value = 0, alternative='two-sided')

    count_A = count.iloc[0]
    count_B = count.iloc[1]

    nobs_A = nobs.iloc[0]
    nobs_B = nobs.iloc[1]

    # CI для разницы p_B - p_A строится с тем же alpha,
    # который используется для проверки гипотезы.

    ci_low, ci_high = confint_proportions_2indep(
        count1 = count_B,
        nobs1 = nobs_B,
        count2 = count_A,
        nobs2 = nobs_A,
        alpha = alpha,
        compare = 'diff',
        method = 'wald'
    )
    p_A = count_A/nobs_A
    p_B = count_B/nobs_B
    difference = p_B - p_A
    uplift = difference / p_A * 100
    print('-' * 60)
    print(f'CR A = {p_A * 100:.2f}%')
    print(f'CR B = {p_B * 100:.2f}%')
    print(f'z = {z_stat:.3f}')
    print(f'p-value = {p_value:.6g}')
    print(f'Разница B - A = {difference * 100:.2f} п.п.')
    print(f'Относительный uplift: {uplift:.2f} %')
    print(f'{(1-alpha) * 100:.2f}% CI = [{ci_low * 100:.2f}; {ci_high * 100:.2f}] п.п.')
    if p_value < alpha:
        print('Статистически значимое различие')
    else:
        print('Статистически значимого различия не обнаружено')
    print('-' * 60)


print('-'*60)
print("Users -> Applications")
ztest_with_ci(funnel['users_application'], funnel['users'], alpha_corrected)
print("Applications -> Approved")
ztest_with_ci(funnel['users_approved'], funnel['users_application'], alpha_corrected)
print("Approved -> Activated")
ztest_with_ci(funnel['users_activated'], funnel['users_approved'], alpha_corrected)
print()

# Основная метрика (Users -> Activated):

print("Users -> Activated")
ztest_with_ci(funnel['users_activated'], funnel['users'], alpha)



