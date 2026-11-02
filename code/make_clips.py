"""Animated MP4 clips for the RAM/SSD + AI bubble video. 1920x1080, 30 fps."""
import sys, math
import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.dates as mdates

D = 'data/'
OUT = 'clips/'
FPS = 30
BG = '#fcfcfb'; INK = '#0b0b0b'; SEC = '#52514e'; MUTED = '#898781'; GRID = '#e1e0d9'; BASE = '#c3c2b7'
BLUE = '#2a78d6'; ORANGE = '#eb6834'; AQUA = '#1baf7a'; YELLOW = '#eda100'; MAGENTA = '#e87ba4'
GREY = '#c3c2b7'; RED = '#d03b3b'
plt.rcParams.update({'font.family': 'sans-serif', 'font.sans-serif': ['DejaVu Sans'], 'figure.facecolor': BG,
                     'axes.facecolor': BG, 'text.color': INK, 'axes.edgecolor': BASE})

def ease(x):  # ease-out cubic, clamped
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3

def prog(t, start, dur):
    return ease((t - start) / dur)

def alpha(t, start, dur=0.5):
    return min(max((t - start) / dur, 0.0), 1.0)

def frame_text(fig, title, subtitle, source, t=99):
    a = 1.0  # titles show from frame 0, so a video's poster matches its first frame
    fig.text(0.06, 0.915, title, fontsize=38, fontweight='bold', color=INK, alpha=a, va='top')
    if subtitle:
        fig.text(0.06, 0.835, subtitle, fontsize=21, color=SEC, alpha=a, va='top')
    if source:
        fig.text(0.06, 0.035, source, fontsize=14, color=MUTED, alpha=a)

def clean(ax, yaxis=False):
    for s in ['top', 'right'] + ([] if yaxis else ['left']):
        ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color(BASE)
    ax.tick_params(length=0, labelsize=17, colors=SEC)
    if not yaxis:
        ax.set_yticks([])

def render(name, duration, draw):
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    writer = animation.FFMpegWriter(fps=FPS, codec='libx264', bitrate=8000,
                                    extra_args=['-pix_fmt', 'yuv420p', '-preset', 'medium'])
    n = int(duration * FPS)
    with writer.saving(fig, OUT + name + '.mp4', dpi=100):
        for i in range(n):
            fig.clf()
            draw(fig, i / FPS)
            writer.grab_frame(facecolor=BG)
    # also save the final frame as a still for the report/slides
    fig.clf(); draw(fig, duration); fig.savefig(OUT + name + '_final.png', dpi=100, facecolor=BG)
    plt.close(fig)
    print('rendered', name)

# ---------------------------------------------------------------- 01 hook
def c01(fig, t):
    frame_text(fig, 'A 32GB DDR5 RAM kit, one year apart', '2x16GB DDR5-4800, US retail price',
               "Source: Tom's Hardware retail prices, compiled by Tech-Insider", t)
    ax = fig.add_axes([0.18, 0.12, 0.64, 0.62]); clean(ax)
    vals = [90, 425]; labs = ['Aug 2025', 'Aug 2026']
    p0 = prog(t, 0.5, 1.2); p1 = prog(t, 1.8, 3.0)
    shown = [vals[0] * p0, vals[1] * p1]
    ax.bar(labs, shown, color=[GREY, BLUE], width=0.5)
    for i, v in enumerate(shown):
        if v > 1:
            ax.text(i, v + 10, f'${v:,.0f}', ha='center', fontsize=34, fontweight='bold', color=INK)
    ax.set_ylim(0, 500)
    ax.tick_params(axis='x', labelsize=22)
    a = alpha(t, 5.0, 0.6)
    ax.text(0.5, 0.92, f'{vals[1] / vals[0]:.1f}x in one year', transform=ax.transAxes, ha='center',
            fontsize=30, color=ORANGE, fontweight='bold', alpha=a)

# ---------------------------------------------------------------- 02 market share
def c02(fig, t):
    frame_text(fig, 'Three companies make almost all of the world\'s DRAM', 'Share of global DRAM revenue, Q2 2026',
               'Source: TrendForce, via The Korea Times (7 Sep 2026)', t)
    ax = fig.add_axes([0.2, 0.14, 0.7, 0.6]); clean(ax)
    names = ['Samsung', 'SK hynix', 'Micron', 'Everyone else']
    vals = [39.4, 24.9, 23.3, 100 - 39.4 - 24.9 - 23.3]
    cols = [BLUE, BLUE, BLUE, GREY]
    y = np.arange(len(names))[::-1]
    for i, (n, v, c) in enumerate(zip(names, vals, cols)):
        p = prog(t, 0.6 + i * 0.5, 1.2)
        ax.barh(y[i], v * p, color=c, height=0.62)
        if p > 0.05:
            ax.text(v * p + 0.8, y[i], f'{v * p:.1f}%', va='center', fontsize=26, fontweight='bold', color=INK)
    ax.set_yticks(y); ax.set_yticklabels(names, fontsize=24, color=INK)
    ax.set_xlim(0, 48); ax.set_xticks([])
    ax.spines['bottom'].set_visible(False)
    a = alpha(t, 3.8, 0.6)
    ax.text(47, y[1], f'Top three:\n{sum(vals[:3]):.1f}%', ha='right', va='center', fontsize=30,
            fontweight='bold', color=BLUE, alpha=a)

# ---------------------------------------------------------------- 03 cause chain
def c03(fig, t):
    frame_text(fig, 'How AI demand pushed memory prices up', 'Four links in the chain', None, t)
    ax = fig.add_axes([0.03, 0.1, 0.94, 0.66]); ax.set_xlim(0, 100); ax.set_ylim(0, 60); ax.axis('off')
    steps = [('AI spending\nexplodes', 'Cloud capex\nprojected +98%\nin 2026'),
             ('Factories shift\nto AI memory', 'HBM + server DRAM\n= 51% of DRAM\nsupply in 2026'),
             ('Cloud giants\nlock in supply', 'Long-term deals;\nsome PC makers get\nreduced allocations'),
             ('SSDs follow', 'Enterprise SSDs\nabsorb NAND flash;\nconsumer supply held back')]
    w, gap = 20, 6.0
    x0 = (100 - (4 * w + 3 * gap)) / 2
    for i, (head, body) in enumerate(steps):
        s = 0.6 + i * 1.8
        a = alpha(t, s, 0.6)
        if a <= 0:
            continue
        x = x0 + i * (w + gap)
        dy = (1 - ease((t - s) / 0.6)) * 3
        box = FancyBboxPatch((x, 8 - dy), w, 44, boxstyle='round,pad=0.4,rounding_size=1.5',
                             fc='white', ec=BLUE if i == 0 else BASE, lw=2.5, alpha=a)
        ax.add_patch(box)
        ax.text(x + w / 2, 48 - dy, str(i + 1), ha='center', va='top', fontsize=26, fontweight='bold', color=BLUE, alpha=a)
        ax.text(x + w / 2, 40 - dy, head, ha='center', va='top', fontsize=23, fontweight='bold', color=INK, alpha=a, linespacing=1.3)
        ax.text(x + w / 2, 25 - dy, body, ha='center', va='top', fontsize=17, color=SEC, alpha=a, linespacing=1.4)
        if i > 0:
            ax.add_patch(FancyArrowPatch((x - gap + 0.8, 30), (x - 0.8, 30), arrowstyle='-|>', mutation_scale=30,
                                         color=MUTED, lw=2.5, alpha=a))
    a = alpha(t, 8.4, 0.6)
    ax.text(50, 1, 'The demand comes from data centres, so weaker PC and phone sales cannot fix it.', ha='center',
            fontsize=21, color=INK, alpha=a, style='italic')

# ---------------------------------------------------------------- 04 hyperscaler capex quarterly (stacked)
def c04(fig, t):
    df = pd.read_csv(D + 'hyperscaler_capex_quarterly.csv')
    cos = [('MSFT', 'Microsoft', BLUE), ('AMZN', 'Amazon', ORANGE), ('GOOG', 'Alphabet', AQUA),
           ('META', 'Meta', YELLOW), ('ORCL', 'Oracle', MAGENTA)]
    frame_text(fig, 'Big Tech\'s quarterly capex nearly quadrupled since 2022',
               'Capital expenditure per quarter, USD billions, stacked by company',
               'Source: Epoch AI, compiled from company SEC filings (cash capex + new finance leases)', t)
    ax = fig.add_axes([0.08, 0.13, 0.74, 0.62]); clean(ax, yaxis=True)
    n = len(df); reveal = 0.5 + 8.0 * prog(t, 0.4, 8.5) * n / n
    k = 0.4; dur = 8.0
    x = np.arange(n)
    for i in range(n):
        p = ease((t - k - i * dur / n) / 0.6)
        if p <= 0:
            continue
        bottom = 0
        for col, lab, c in cos:
            v = df[col].iloc[i] / 1000 * p
            ax.bar(i, v, bottom=bottom, color=c, width=0.72, edgecolor=BG, linewidth=1.5)
            bottom += v
    ax.set_xticks(x[::4]); ax.set_xticklabels([q[:4] for q in df.quarter[::4]], fontsize=18)
    ax.set_ylim(0, 160); ax.set_yticks([0, 50, 100, 150])
    ax.set_yticklabels(['$0', '$50B', '$100B', '$150B'], fontsize=17)
    ax.grid(axis='y', color=GRID); ax.set_axisbelow(True)
    ax.set_xlim(-0.7, n - 0.3)
    # legend (direct labels at the right of the final bar)
    a = alpha(t, 7.5, 0.6)
    bottom = 0
    for col, lab, c in cos:
        v = df[col].iloc[-1] / 1000
        fig.text(0.835, 0.13 + (bottom + v / 2) / 160 * 0.62, lab, fontsize=19, color=INK, va='center', alpha=a)
        fig.patches.append(matplotlib.patches.Rectangle((0.825, 0.13 + (bottom + v / 2) / 160 * 0.62 - 0.006), 0.007, 0.012,
                                                        transform=fig.transFigure, fc=c, alpha=a))
        bottom += v
    a2 = alpha(t, 9.2, 0.6)
    first, last = df.total_musd.iloc[0] / 1000, df.total_musd.iloc[-1] / 1000
    ax.text(0.02, 0.95, f'\\${first:.1f}B per quarter (Q1 2022) → \\${last:.1f}B (Q4 2025): {last / first:.1f}x',
            transform=ax.transAxes, fontsize=24, fontweight='bold', color=INK, va='top', alpha=a2)

# ---------------------------------------------------------------- 05 DDR4 price cycle (line)
EVENTS = [('2022-11-30', '1  ChatGPT launches (Nov 2022)', 27.5, 'left'),
          ('2025-06-15', '2  Makers announce DDR4 phase-out (Jun 2025)', 23.0, 'right'),
          ('2025-12-17', '3  Reports: Nvidia to cut RTX 50 supply 30-40% (Dec 2025)', 19.0, 'right')]

def c05(fig, t):
    df = pd.read_csv(D + 'ddr4_contract_price.csv')
    df['date'] = pd.to_datetime(df.month + '-15')
    frame_text(fig, 'A memory chip\'s price: from bust to 20x boom',
               'DDR4 8Gb DRAM chip, monthly average contract price (USD); dots = months with a reported price',
               'Source: DRAMeXchange contract prices as reported by Korean press, compiled by Silicon Analysts (Oct 2026)', t)
    ax = fig.add_axes([0.08, 0.13, 0.86, 0.62]); clean(ax, yaxis=True)
    xs = mdates.date2num(df.date.values); ys = df.contract_usd.values
    p = prog(t, 0.5, 9.0)
    xend = xs[0] + (xs[-1] - xs[0]) * p
    # interpolate the line up to xend
    mask = xs <= xend
    lx = list(xs[mask]); ly = list(ys[mask])
    if xend < xs[-1] and mask.sum() >= 1:
        j = mask.sum()
        f = (xend - xs[j - 1]) / (xs[j] - xs[j - 1])
        lx.append(xend); ly.append(ys[j - 1] + f * (ys[j] - ys[j - 1]))
    # shade bust period
    ax.axvspan(mdates.date2num(pd.Timestamp('2022-01-01')), mdates.date2num(pd.Timestamp('2023-12-31')),
               color=GRID, alpha=0.45 * alpha(t, 0.5))
    ax.text(mdates.date2num(pd.Timestamp('2022-05-01')), 27.5, 'Bust', ha='center', fontsize=22, color=SEC, alpha=alpha(t, 1.5))
    # event markers: each appears as the drawing line reaches its date
    for d, lab, ty, ha in EVENTS:
        xe = mdates.date2num(pd.Timestamp(d))
        te = 0.5 + 9.0 * (xe - xs[0]) / (xs[-1] - xs[0])
        a = alpha(t, te, 0.5)
        if a <= 0:
            continue
        ax.axvline(xe, color=MUTED, ls='--', lw=1.6, alpha=a, zorder=1)
        ax.text(xe + (8 if ha == 'left' else -8), ty, lab, ha=ha, va='center', fontsize=17, color=INK, alpha=a,
                bbox=dict(boxstyle='round,pad=0.3', fc=BG, ec=BASE, lw=1, alpha=a))
    ax.plot(lx, ly, color=BLUE, lw=4, solid_capstyle='round')
    ax.scatter(xs[mask], ys[mask], s=70, color=BLUE, zorder=3, edgecolors=BG, linewidths=2)
    ax.set_ylim(0, 30); ax.set_yticks([0, 5, 10, 15, 20, 25])
    ax.set_yticklabels([f'${v}' for v in [0, 5, 10, 15, 20, 25]], fontsize=17)
    ax.grid(axis='y', color=GRID); ax.set_axisbelow(True)
    ax.set_xlim(mdates.date2num(pd.Timestamp('2021-11-01')), mdates.date2num(pd.Timestamp('2026-12-15')))
    ax.xaxis.set_major_locator(mdates.YearLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    # annotations
    tr = df.contract_usd.idxmin()
    a = alpha(t, 3.2, 0.6)
    if a > 0:
        drop = 1 - df.contract_usd[tr] / df.contract_usd.iloc[0]
        ax.annotate(f'${df.contract_usd[tr]:.2f} in {df.date[tr]:%b %Y}\n-{drop:.0%} from Jan 2022', (xs[tr], ys[tr]),
                    xytext=(xs[tr] + 60, 9), fontsize=20, color=INK, alpha=a,
                    arrowprops=dict(arrowstyle='-', color=MUTED, lw=1.5, alpha=a))
    a = alpha(t, 9.6, 0.6)
    if a > 0:
        ax.annotate(f'${ys[-1]:.0f} in {df.date.iloc[-1]:%b %Y}\n{ys[-1] / ys[tr]:.0f}x the 2023 low', (xs[-1], ys[-1]),
                    xytext=(mdates.date2num(pd.Timestamp('2026-04-01')), 26.6), fontsize=22, fontweight='bold', color=BLUE, alpha=a, ha='right', va='center',
                    bbox=dict(boxstyle='round,pad=0.25', fc=BG, ec='none', alpha=a),
                    arrowprops=dict(arrowstyle='-', color=BLUE, lw=1.5, alpha=a))

# ---------------------------------------------------------------- 06 consumer impact (signed bars)
def c06(fig, t):
    frame_text(fig, 'Consumers pay: pricier PCs, fewer devices sold', 'Forecast change in 2026 vs 2025',
               'Sources: Gartner (Feb 2026) via Shattered.io; Counterpoint Research via InfotechLead', t)
    ax = fig.add_axes([0.28, 0.14, 0.62, 0.6]); clean(ax)
    rows = [('Average PC price', 17.0), ('PC shipments', -10.4), ('Smartphone shipments', -13.9)]
    y = np.arange(len(rows))[::-1]
    for i, (lab, v) in enumerate(rows):
        p = prog(t, 0.6 + i * 0.8, 1.3)
        c = ORANGE if v > 0 else BLUE
        ax.barh(y[i], v * p, color=c, height=0.55)
        if p > 0.05:
            if v > 0:
                ax.text(v * p + 0.6, y[i], f'{v * p:+.1f}%', va='center', ha='left', fontsize=28, fontweight='bold', color=INK)
            else:
                ax.text(v * p + 0.6, y[i], f'{v * p:+.1f}%', va='center', ha='left', fontsize=26, fontweight='bold', color='white')
    ax.axvline(0, color=SEC, lw=1.5)
    ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=24, color=INK)
    ax.set_xlim(-20, 22); ax.set_xticks([]); ax.spines['bottom'].set_visible(False)
    a = alpha(t, 3.8, 0.6)
    fig.text(0.28, 0.08, 'Memory rises from 16% to 23% of a PC\'s parts cost (Gartner)', fontsize=21, color=SEC, alpha=a)

# ---------------------------------------------------------------- 07 SK hynix profit (bars about zero)
def c07(fig, t):
    df = pd.read_csv(D + 'skhynix_operating_profit.csv')
    v = df.operating_profit_krw_bn.values / 1000
    frame_text(fig, 'For memory makers, the bust became a bonanza',
               'SK hynix quarterly operating profit, trillion Korean won',
               'Source: SK hynix quarterly results releases (4Q22 approx., via DatacenterDynamics)', t)
    ax = fig.add_axes([0.08, 0.13, 0.86, 0.62]); clean(ax, yaxis=True)
    n = len(df)
    for i in range(n):
        p = ease((t - 0.5 - i * 0.45) / 0.6)
        if p <= 0:
            continue
        c = RED if v[i] < 0 else BLUE
        ax.bar(i, v[i] * p, color=c, alpha=0.85 if v[i] < 0 else 1, width=0.7)
    ax.axhline(0, color=SEC, lw=1.5)
    ax.set_xticks(range(n)); ax.set_xticklabels(df.quarter, fontsize=14, rotation=0)
    ax.set_ylim(-8, 68); ax.set_yticks([0, 20, 40, 60]); ax.set_yticklabels(['0', '20', '40', '60'], fontsize=17)
    ax.grid(axis='y', color=GRID); ax.set_axisbelow(True)
    lo = int(np.argmin(v)); hi = n - 1
    a = alpha(t, 0.5 + lo * 0.45 + 0.6, 0.5)
    ax.text(lo, 4, f'Losses through 2023\n(worst: {v[lo]:.1f}tn in {df.quarter[lo]})', ha='center', va='bottom', fontsize=18, color=RED, alpha=a)
    a = alpha(t, 0.5 + hi * 0.45 + 0.6, 0.5)
    ax.text(hi - 0.5, v[hi] + 1, f'+{v[hi]:.1f}tn profit ({df.quarter[hi]})\n76% operating margin', ha='right', va='bottom',
            fontsize=21, fontweight='bold', color=BLUE, alpha=a)

# ---------------------------------------------------------------- 08 annual capex projection
def c08(fig, t):
    frame_text(fig, 'Big Tech capex is set to double to about $1 trillion in 2026',
               'Hyperscaler capital expenditure per year; 2026-2028 are UBS estimates',
               'Source: UBS estimates via 24/7 Wall St. / Yahoo Finance (22 Aug 2026)', t)
    ax = fig.add_axes([0.12, 0.12, 0.76, 0.62]); clean(ax)
    yrs = ['2025', '2026', '2027', '2028']; cap = [492, 1009, 1447, 1619]
    for i, c in enumerate(cap):
        p = prog(t, 0.5 + i * 0.7, 1.2)
        col = BLUE if i == 1 else GREY
        ax.bar(i, c * p, color=col, width=0.55)
        if p > 0.05:
            lab = f'${c * p / 1000:.2f}T' if c * p >= 1000 else f'${c * p:.0f}B'
            ax.text(i, c * p + 30, lab, ha='center', fontsize=28, fontweight='bold', color=INK)
    ax.set_xticks(range(4)); ax.set_xticklabels(yrs, fontsize=22)
    ax.set_ylim(0, 1900)
    a = alpha(t, 0.8, 0.5)
    ax.axvline(0.5, color=MUTED, ls='--', lw=1.8, alpha=a)
    ax.text(0.44, 1800, 'Actual', ha='right', fontsize=19, color=SEC, alpha=a)
    ax.text(0.56, 1800, 'UBS estimates', ha='left', fontsize=19, color=SEC, alpha=a)
    a = alpha(t, 4.4, 0.6)
    ax.text(3.35, 700, 'Amazon, Alphabet and\nMicrosoft: capex = ~102%\nof cloud revenue in 2026', ha='right',
            fontsize=19, color=INK, alpha=a)

# ---------------------------------------------------------------- 09 valuations
def c09(fig, t):
    frame_text(fig, 'Not 2000 again? Valuations are far below the dot-com peak',
               'Price-to-earnings multiple (x)', 'Source: IoT Analytics, "Are we in an AI bubble?" (6 Oct 2026)', t)
    ax = fig.add_axes([0.3, 0.16, 0.6, 0.56]); clean(ax)
    rows = [('Cisco at the 2000 peak', 200, None), ('AI leaders today\n(Alphabet, Meta, Microsoft, NVIDIA)', 23.5, (22, 25))]
    y = [1, 0]
    for i, (lab, v, rng) in enumerate(rows):
        p = prog(t, 0.6 + i * 1.4, 1.5)
        ax.barh(y[i], v * p, color=GREY if i == 0 else BLUE, height=0.5)
        if p > 0.05:
            txt = f'~{v * p:.0f}x' if rng is None else f'{rng[0]}-{rng[1]}x forward'
            ax.text(v * p + 3, y[i], txt, va='center', fontsize=28, fontweight='bold', color=INK)
    ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=21, color=INK)
    ax.set_xlim(0, 240); ax.set_xticks([]); ax.spines['bottom'].set_visible(False)
    a = alpha(t, 4.2, 0.6)
    fig.text(0.3, 0.08, 'But even this analysis expects Big Tech\'s AI returns to fall below target from 2028.',
             fontsize=20, color=SEC, alpha=a, style='italic')

# ---------------------------------------------------------------- 10 scenarios
def c10(fig, t):
    frame_text(fig, 'Memory prices are a bet on AI spending', 'Three scenarios (our reasoning, not a forecast)', None, t)
    ax = fig.add_axes([0.03, 0.08, 0.94, 0.68]); ax.set_xlim(0, 100); ax.set_ylim(0, 60); ax.axis('off')
    cards = [('Boom continues', 'AI capex keeps rising\n(UBS: $1.45T in 2027)', 'RAM stays expensive\nthrough 2027', '↑', ORANGE),
             ('Slowdown', 'Capex growth flattens\nas returns disappoint', 'New fabs meet softer\ndemand; prices drift down', '↘', YELLOW),
             ('Bubble deflates', 'Data-centre orders\nare cut sharply', 'Prices could crash,\nas they halved in 2022', '↓', BLUE)]
    w, gap = 28, 5
    x0 = (100 - (3 * w + 2 * gap)) / 2
    for i, (head, spend, mem, arrow, c) in enumerate(cards):
        s = 0.6 + i * 1.6
        a = alpha(t, s, 0.6)
        if a <= 0:
            continue
        x = x0 + i * (w + gap); dy = (1 - ease((t - s) / 0.6)) * 3
        ax.add_patch(FancyBboxPatch((x, 4 - dy), w, 50, boxstyle='round,pad=0.4,rounding_size=1.5', fc='white', ec=BASE, lw=2.5, alpha=a))
        ax.text(x + w / 2, 51 - dy, head, ha='center', va='top', fontsize=27, fontweight='bold', color=INK, alpha=a)
        ax.text(x + 2, 42 - dy, 'AI spending', fontsize=16, color=MUTED, alpha=a, va='top')
        ax.text(x + 2, 38 - dy, spend, fontsize=19, color=INK, alpha=a, va='top', linespacing=1.35)
        ax.text(x + 2, 25 - dy, 'Memory prices', fontsize=16, color=MUTED, alpha=a, va='top')
        ax.text(x + 2, 21 - dy, mem, fontsize=19, color=INK, alpha=a, va='top', linespacing=1.35)
        ax.text(x + w - 2, 26 - dy, arrow, fontsize=60, color=c, alpha=a, ha='right', va='top', fontweight='bold')

def c11(fig, t):
    cap = pd.read_csv(D + 'hyperscaler_capex_quarterly.csv')
    cap['date'] = pd.PeriodIndex(cap.quarter.str[:4] + 'Q' + cap.quarter.str[-1], freq='Q').to_timestamp() + pd.Timedelta(days=45)
    pr = pd.read_csv(D + 'ddr4_contract_price.csv'); pr['date'] = pd.to_datetime(pr.month + '-15')
    frame_text(fig, 'AI spending rose first; memory prices followed',
               'Same timeline: Big Tech capex per quarter (top) and DDR4 chip contract price (bottom)',
               'Sources: Epoch AI (SEC filings); DRAMeXchange via Silicon Analysts. Timing is consistent with AI demand driving prices, not proof on its own.', t)
    x0, x1 = mdates.date2num(pd.Timestamp('2021-11-01')), mdates.date2num(pd.Timestamp('2026-12-15'))
    p = prog(t, 0.6, 8.5); cur = x0 + (x1 - x0) * p
    a1 = fig.add_axes([0.08, 0.47, 0.86, 0.30]); clean(a1, yaxis=True)
    a2 = fig.add_axes([0.08, 0.11, 0.86, 0.30]); clean(a2, yaxis=True)
    cx = mdates.date2num(cap.date); cv = cap.total_musd.values / 1000
    m = cx <= cur
    a1.bar(cx[m], cv[m], width=70, color=ORANGE)
    a1.set_ylim(0, 160); a1.set_yticks([0, 50, 100, 150]); a1.set_yticklabels(['$0', '$50B', '$100B', '$150B'], fontsize=15)
    a1.text(0.0, 1.02, 'Capex per quarter', transform=a1.transAxes, fontsize=18, color=SEC)
    px = mdates.date2num(pr.date); pv = pr.contract_usd.values
    m2 = px <= cur
    lx, ly = list(px[m2]), list(pv[m2])
    if m2.sum() and m2.sum() < len(px):
        j = m2.sum(); f = (cur - px[j - 1]) / (px[j] - px[j - 1]); lx.append(cur); ly.append(pv[j - 1] + f * (pv[j] - pv[j - 1]))
    a2.plot(lx, ly, color=BLUE, lw=3.5); a2.scatter(px[m2], pv[m2], s=45, color=BLUE, zorder=3, edgecolors=BG, linewidths=1.5)
    a2.set_ylim(0, 30); a2.set_yticks([0, 10, 20, 30]); a2.set_yticklabels(['$0', '$10', '$20', '$30'], fontsize=15)
    a2.text(0.0, 1.02, 'DDR4 8Gb contract price', transform=a2.transAxes, fontsize=18, color=SEC)
    for ax in (a1, a2):
        ax.set_xlim(x0, x1); ax.grid(axis='y', color=GRID); ax.set_axisbelow(True)
        ax.xaxis.set_major_locator(mdates.YearLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        if p < 1:
            ax.axvline(cur, color=MUTED, lw=1.2, alpha=0.6)
    a1.tick_params(labelbottom=False)
    a = alpha(t, 0.6 + 8.5 * (mdates.date2num(pd.Timestamp('2024-06-01')) - x0) / (x1 - x0), 0.6)
    a1.text(mdates.date2num(pd.Timestamp('2023-10-01')), 120, 'Capex takes off\nfrom 2024', fontsize=19, fontweight='bold', color=ORANGE, alpha=a, ha='right')
    a = alpha(t, 0.6 + 8.5 * (mdates.date2num(pd.Timestamp('2025-10-01')) - x0) / (x1 - x0), 0.6)
    a2.text(mdates.date2num(pd.Timestamp('2025-04-01')), 18, 'Prices follow\nfrom mid-2025', fontsize=19, fontweight='bold', color=BLUE, alpha=a, ha='right')

CLIPS = {'01_hook_ram_kit': (c01, 7), '02_market_share': (c02, 6.5), '03_cause_chain': (c03, 11),
         '04_capex_quarterly': (c04, 11), '05_dram_price_cycle': (c05, 14), '06_consumer_impact': (c06, 6.5),
         '07_skhynix_profit': (c07, 9.5), '08_capex_projection': (c08, 7), '09_valuations': (c09, 7),
         '10_scenarios': (c10, 8), '11_capex_vs_price': (c11, 11)}

if __name__ == '__main__':
    which = sys.argv[1:] or list(CLIPS)
    for k in which:
        fn, dur = CLIPS[k]
        render(k, dur, fn)
