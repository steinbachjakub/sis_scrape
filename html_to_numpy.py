import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np


results = pd.read_csv("data.csv")
index_map = pd.isna(results[["1. PP", "2. PP"]]).sum(axis=1) < 1
results = results[index_map]
results["Celkem"] = results["1. PP"] + results["2. PP"]
results["Zápočet"] = results["Celkem"] >= 100
results["Souhrnný test"] = (results["Zápočet"] == False) & (results["Celkem"] >= 60)
results["Příjmení"] = results["Vyučující"].apply(lambda x: x[:x.find(" ")])
results["Program"] = results["Obor"].apply(lambda x: x[:4])
map_faculty = {"1": "FCHT", "2": "FTOP", "3": "FPBT", "4": "FCHI", "9": "EKO"}
results["Fakulta"] = results["Obor"].apply(lambda x: x[1])
results["Fakulta"] = results["Fakulta"].map(map_faculty)

agg_func = {'Celkem': ['mean', 'median']}
# agg_func = {'Celkem': ['mean', 'median', 'min', 'max', 'std', 'var']}

teachers_agg = results.groupby("Příjmení").agg(agg_func).sort_values(('Celkem', 'median'))

program_agg = results.groupby("Program").agg(agg_func).sort_values(('Celkem', 'median'))
faculty_agg = results.groupby("Fakulta").agg(agg_func).sort_values(('Celkem', 'median'))

print(teachers_agg[('Celkem', 'median')])

fig = plt.figure(figsize=(12, 6))
gs = GridSpec(1, 5, figure=fig)
ax0 = fig.add_subplot(gs[0:2])
ax0.bar(teachers_agg.index, teachers_agg[('Celkem', 'median')], fc="darkgreen", ec="black")
ax0.set_xticklabels(ax0.get_xticklabels(), rotation=90)
ax0.set_title("Medián celkového počtu bodů pro vyučující")
ax0.axhline(100, color="black", linestyle="--")

ax1 = fig.add_subplot(gs[2:4])
ax1.bar(program_agg.index, program_agg[('Celkem', 'median')], fc="crimson", ec="black")
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90)
ax1.set_title("Medián celkového počtu bodů pro obory")
ax1.axhline(100, color="black", linestyle="--")

ax2 = fig.add_subplot(gs[4])
ax2.bar(faculty_agg.index, faculty_agg[('Celkem', 'median')], fc="darkblue", ec="black")
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90)
ax2.set_title("Medián celkového\npočtu bodů\npro fakulty", ha="center")
ax2.axhline(100, color="black", linestyle="--")
plt.subplots_adjust(bottom=0.2, top=0.85, left=0.1, right=0.95)


for ax in [ax0, ax1, ax2]:
    ax.set_yticks(np.linspace(0, max(ax0.get_yticks().max(), ax1.get_yticks().max(), ax2.get_yticks().max()), 5))

# axes = teachers_agg[teachers_agg.columns].plot.bar(rot=90, subplots=True)
# # axes[1].legend(loc=2)
# plt.subplots_adjust(bottom=0.4, top=0.95, left=0.05, right=0.95)
plt.show()

