import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('us_budget_expenses.csv')
number_columns = [str(i) for i in range(1976,2013)]

def string_to_number(s):
    return int(s.replace(",",""))

def get_first_digit(num):
    number = string_to_number(num)
    return int(str(abs(number))[0])

def get_numbers_for_dataframe(frame):
    years = range(1976,2013)
    all_numbers = []
    for y in years:
        for i in frame[str(y)]:
            all_numbers.append(get_first_digit(i))
    return [x for x in all_numbers if x != 0]

def get_numbers_for_dataframe_and_year(frame, year):
    all_numbers = []
    for i in frame[str(year)]:
        all_numbers.append(get_first_digit(i))
    return [x for x in all_numbers if x != 0]

#remove zeros
benford=[math.log10(1+1.0/i) for i in xrange(1,10)]
width = 0.3
x = np.arange(1,10)

fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.bar(x, benford, width, color='r', align='center')
ax1.set_xticks(x)
ax1.set_title("Theoretical Benford", fontsize=20)

fig3 = plt.figure()
ax3 = fig3.add_subplot(111)
ax3.hist(get_numbers_for_dataframe_and_year(df, 2002), rwidth=width, align='left', normed=True, bins=range(1,11), color='g', label='US Budget')
ax3.bar(x+width+.05, benford, width, color='r', align='center', label='Theoretical Benford')
ax3.set_xticks(x)
ax3.legend()
ax3.set_title("Benford vs. Entire US Budget", fontsize=20)


# Small Multiple for each agency
df['transformed_2012'] = df['2012'].map(lambda x: int(x.replace(",","")))
summarized_2012_agencies = df.groupby('Agency Name')['transformed_2012'].sum()
summarized_2012_agencies.sort([1], ascending=False)
agency_names = summarized_2012_agencies.index.values
fig4 = plt.figure(figsize=(10,60))
benford=[math.log10(1+1.0/i) for i in xrange(1,10)]
width = 0.3
x = np.arange(1,10)
for n, name in enumerate(agency_names[:26]):
    print name
    if len(get_numbers_for_dataframe(df[df['Agency Name'] == name])) > 0:
        ax = plt.subplot(13,2,n+1)
        numbers_for_graph = get_numbers_for_dataframe(df[df['Agency Name'] == name])
        plt.hist(numbers_for_graph, rwidth=width, align='left', normed=True, bins=range(1,11), color='g', label=name)
        plt.bar(x+width+.05, benford, width, color='r', align='center', label='Theoretical Benford')
        ax.text(1, 1, "n = " + str(len(numbers_for_graph)), verticalalignment='top', horizontalalignment='right')
        plt.xticks(x) 
        ax.set_title(name)

fig4.set_tight_layout(True)


plt.draw()

plt.tight_layout()


fig5 = plt.figure(figsize=(10,54))
benford=[math.log10(1+1.0/i) for i in xrange(1,10)]
width = 0.3
x = np.arange(1,10)
year_range = range(1977,2013)
year_range.reverse()
for number, n in enumerate(year_range):
    ax2 = plt.subplot(18,2, number+1)
    plt.hist(get_numbers_for_dataframe_and_year(df, n), rwidth=width, align='left', normed=True, bins=range(1,11), color='g', label=str(n))
    plt.bar(x+width+.05, benford, width, color='r', align='center', label='Theoretical Benford')
    plt.xticks(x)
    ax2.set_title(str(n))
fig5.set_tight_layout(True)
plt.draw()


plt.tight_layout()
