import matplotlib.pyplot as plt
import numpy as np

# player data
players = ['Dembélé', 'Salah', 'Yamal', 'Raphinha']
g_per_90 = [1.09, 0.77, 0.28, 0.57]
a_per_90 = [0.41, 0.48, 0.47, 0.35]
drib_per_90 = [2.18, 1.55, 5.07, 1.65]
xg_total = [16.6, 25.2, 9.8, 19.2]
xa_total = [8.2, 14.2, 13.9, 12.7]
total_ga = [29, 47, 24, 29]
all_comp_ga = [51, 57, 43, 59]

fig = plt.figure(figsize=(18, 12))
ax1 = plt.subplot(2, 2, 1)
x = np.arange(len(players))
width = 0.25

ax1.bar(x - width, g_per_90, width, label='G/90', color='red', alpha=0.8)
ax1.bar(x, a_per_90, width, label='A/90', color='blue', alpha=0.8)
ax1.bar(x + width, drib_per_90, width, label='Succ. Dribbles/90', color='green', alpha=0.8)

ax1.set_xlabel('Players')
ax1.set_ylabel('Per 90 Minutes')
ax1.set_title('League Stats')
ax1.set_xticks(x)
ax1.set_xticklabels(players)
ax1.legend()

for i, (g, a, d) in enumerate(zip(g_per_90, a_per_90, drib_per_90)):
    ax1.text(i - width, g + 0.05, f'{g:.2f}', ha='center', fontsize=9)
    ax1.text(i, a + 0.05, f'{a:.2f}', ha='center', fontsize=9)
    ax1.text(i + width, d + 0.1, f'{d:.2f}', ha='center', fontsize=9)

ax2 = plt.subplot(2, 2, 2)
x2 = np.arange(len(players))
ax2.bar(x2, total_ga, label='League G+A', alpha=0.8, color='orange')
ax2.bar(x2, [all_comp_ga[i] - total_ga[i] for i in range(len(players))],
        bottom=total_ga, label='Other Comps G+A', alpha=0.8, color='purple')

ax2.set_xlabel('Players')
ax2.set_ylabel('Goal Contributions')
ax2.set_title('Total G+A Breakdown')
ax2.set_xticks(x2)
ax2.set_xticklabels(players)
ax2.legend()
ax3 = plt.subplot2grid((2, 2), (1, 0), colspan=2, projection='polar')
metrics = ['G/90', 'A/90', 'xG', 'xA', 'Drib/90']
values = np.array([g_per_90, a_per_90, xg_total, xa_total, drib_per_90]).T
values_norm = (values - values.min(axis=0)) / (values.max(axis=0) - values.min(axis=0))

angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
angles += angles[:1]  # Close loop

colors = ['red', 'blue', 'green', 'orange']
for i, player in enumerate(players):
    vals = np.append(values_norm[i], values_norm[i][0])
    ax3.plot(angles, vals, 'o-', linewidth=2, label=player, color=colors[i])
    ax3.fill(angles, vals, alpha=0.15, color=colors[i])

ax3.set_xticks(angles[:-1])
ax3.set_xticklabels(metrics)
ax3.set_ylim(0, 1)
ax3.set_title('Performance Radar', pad=20)
ax3.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
fig.suptitle('Ballon d\'Or 2025 Contenders', fontsize=16, fontweight='bold')

plt.tight_layout()
plt.savefig('ballon_dor_2025_comparison.png')
plt.show()