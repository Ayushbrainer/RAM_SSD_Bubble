import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
BLUE='#2a78d6'; GREY='#c3c2b7'; INK='#0b0b0b'; SEC='#52514e'; MUTED='#898781'; BASE='#c3c2b7'
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['DejaVu Sans'],'font.size':11,
  'axes.edgecolor':BASE,'xtick.color':SEC,'ytick.color':MUTED,'axes.grid':False})
def clean(ax):
    for s in ['top','right','left']: ax.spines[s].set_visible(False)
    ax.tick_params(length=0); ax.set_yticks([])

# Figure 1: retail RAM kit
fig, ax = plt.subplots(figsize=(6.2,3.0))
lab=['Aug 2025','Aug 2026']; v=[90,425]
ax.bar(lab, v, color=[GREY,BLUE], width=0.5)
for i,x in enumerate(v): ax.text(i, x+10, f'${x}', ha='center', fontsize=12, fontweight='bold', color=INK)
ax.set_ylim(0,480); clean(ax)
ax.text(0.5,0.9,f'{v[1]/v[0]:.1f}x in one year',transform=ax.transAxes,ha='center',color=SEC)
fig.tight_layout(); fig.savefig('figures/ram_kit.pdf'); plt.close(fig)

# Figure 2: hyperscaler capex
fig, ax = plt.subplots(figsize=(6.2,3.2))
yrs=['2025','2026','2027','2028']; cap=[492,1009,1447,1619]
ax.bar(yrs, cap, color=[GREY,BLUE,GREY,GREY], width=0.55)
for i,x in enumerate(cap): ax.text(i, x+30, f'${x/1000:.2f}T' if x>=1000 else f'${x}B', ha='center', fontsize=11, fontweight='bold', color=INK)
ax.axvline(0.5, color=MUTED, ls='--', lw=1)
ax.text(0.45, 1780, 'Actual', ha='right', color=SEC, fontsize=10); ax.text(0.55, 1780, 'UBS estimates', ha='left', color=SEC, fontsize=10)
ax.set_ylim(0,1900); clean(ax)
fig.tight_layout(); fig.savefig('figures/capex.pdf'); plt.close(fig)
print('ok')
