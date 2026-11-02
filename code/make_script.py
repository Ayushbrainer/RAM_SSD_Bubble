"""Build video_script.tex from code/narration.json (the same narration used for the deck's speaker notes).
Run from the repo root:  python code/make_script.py   then compile video_script.tex with pdflatex."""
import json, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
n = json.load(open(os.path.join(ROOT, 'code', 'narration.json'), encoding='utf-8'))

def tex(s):
    for a, b in [('\\', '\\textbackslash{}'), ('&', '\\&'), ('%', '\\%'), ('$', '\\$'), ('_', '\\_'), ('#', '\\#')]:
        s = s.replace(a, b)
    return s

PARTS = [('Ayush Bhatt', 'Part 1: Ayush Bhatt', 'Introduction and the data story'),
         ('Bu Dinglin', 'Part 2: Bu Dinglin', 'Impact, the bubble question and conclusion')]

body = []
for who, title, sub in PARTS:
    scenes = [s for s in n if s['speaker'] == who]
    words = sum(len(s['text'].split()) for s in scenes)
    start, end = scenes[0]['time'].split('-')[0], scenes[-1]['time'].split('-')[1]
    body.append(f"\\section*{{{title}}}\n{{\\color{{muted}}{sub} \\quad$\\cdot$\\quad {start}--{end} \\quad$\\cdot$\\quad about {words} words}}\n")
    for s in scenes:
        clip = f"\\texttt{{{tex(s['clip'])}.mp4}}: " if s.get('clip') else ''
        body.append(f"\\scene{{{tex(s['scene'])}}}{{{s['time'].replace('-', '--')}}}\n{{{clip}{tex(s['screen'])}}}\n{{``{tex(s['text'])}''}}\n")

total = sum(len(s['text'].split()) for s in n)
doc = r"""\documentclass[11pt]{article}
\input{style}
\geometry{top=1.7cm,bottom=1.7cm}
\titlespacing*{\subsection}{0pt}{0.6em}{0.2em}
\setlength{\parskip}{0.35em}

\usepackage{needspace}
\newcommand{\scene}[4]{%
  \needspace{7\baselineskip}\subsection*{#1 \hfill {\normalfont\color{muted}\small #2}}
  {\small\color{muted}\textbf{On screen:} #3}\par\vspace{-0.2em}
  \begin{keybox}#4\end{keybox}}

\begin{document}

\doctitle{Video Script: The 2026 Memory Price Surge and the AI Bubble}
{14 slides, 11 animated clips, about 5 minutes}
{Group [\_\_\_] \quad$\cdot$\quad Ayush Bhatt (G2610412E) \& Bu Dinglin (\rule{1.8cm}{0.4pt}) \quad$\cdot$\quad Data as of 26 October 2026}

\textbf{How to use.} Present \texttt{RAM\_AI\_Bubble.pptx} and record it with PowerPoint's Record feature. Each slide's speaker notes hold the same narration, marked with who speaks. Ayush opens and takes the data story; Bu Dinglin takes over at Scene 6 and closes. About """ + str(total) + r""" words, roughly 5 minutes including the clips, inside the 6-minute cap. Target times assume about 140 words a minute.

""" + "\n".join(body) + r"""
\section*{Production notes}
\begin{itemize}
  \item \textbf{Numbers to land:} 4.7x (Scene 1), 20x (Scene 5), the 76\% margin (Scene 8). Pause after each.
  \item \textbf{Handover:} Ayush ends Scene 5 with ``Over to Dinglin''; Dinglin opens Scene 6 with ``Thanks, Ayush''.
  \item \textbf{Hedges to keep:} the RTX 50 cut was \emph{reported} and Nvidia denied a full pause; Scene 6's ``timing alone doesn't prove cause''; every ``if'' in Scene 10.
  \item \textbf{Rounded for speech:} ``nearly 88\%'' = 87.6\%; ``38'' and ``141 billion'' = \$37.6B and \$140.6B; ``about 10\%'' = 10.4\%; ``nearly 14\%'' = 13.9\%; ``almost four times'' = 3.7x.
\end{itemize}

\end{document}
"""
open(os.path.join(ROOT, 'video_script.tex'), 'w', encoding='utf-8').write(doc)
print('wrote video_script.tex')
