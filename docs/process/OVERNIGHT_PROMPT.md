# Overnight prompt: organise everything, test the core finding, then write report v1

Read `docs/process/project_rules.md` and this file. Then work through Stages 1–6 in order, without asking questions. Commit after every stage. If a gate fails, write `analysis/output/STOP.md` and stop.

## Where we stand (verified, committed in 3e8ecd7)

- **Confirmatory study.** The primary strategy, A3, has a test Sharpe of −0.58. The verdict is "Do not implement" and it stands.
- **v2 (post-hoc).** Four variants were frozen before running and all four are reported. None passes the reading rule; the deflated Sharpe is at most 0.18.
- **V2a, the declared headline (wage growth).** Test Sharpe +0.16, with an IC t of 2.04 and a placebo p of 0.02. But its alpha t is only 0.29: it is mostly a growth/momentum tilt. Its Sharpe over the last 18 months is −1.71.
- **V2c (wage growth + momentum).** Test Sharpe +0.35.
- **V2d, the strongest finding.** V2d is −(hires + quits), held for 12 months. It is the long-horizon investment/cost channel that the thesis and Belo–Lin–Bazdresch predict.
  - It is the only variant that is positive in every window: research +0.50, test +0.29, last 18 months +0.29.
  - Its 12-month IC in the test window is 0.096 (t 2.43).
  - Its full-sample alpha t is 1.96.
  - The pre-declared 1-month placebo gives p = 0.85. The horizon-matched placebo, added post-hoc, gives p = 0.06 in the test window and 0.04 on the full sample.
- **The thesis result in one sentence:** labor flows carry industry information as slow cost news (12 months, q-theory sign), not as fast demand news (1 month).

---

## Stage 1: The Results Book (organise everything before any report text)

Create `results/` containing `RESULTS_BOOK.md` and a compiled `results_book.pdf`. The PDF uses the **house template** (Appendix A: `\input{../report/preamble}`, with `\renewcommand{\ReportTitle}{Follow the Workers: Results Book}`), `\input`s every table and includes every figure. Piero reads this in the morning, so it must be complete and easy to scan.

1. **Verdict page.** The one-paragraph story, the scoreboard, and the verdict for each strategy.
2. **Scoreboard.** One table covering A0, A1, A1-T, A3, A4 (confirmatory, Sonnet study), the Opus follow-up (exploratory) and V2a–V2d (post-hoc). Columns: label, research Sharpe, test Sharpe, full-sample Sharpe, last-18-month Sharpe, IC (t), alpha (t), placebo p, deflated Sharpe, verdict.
3. **Figures.** Every figure, each with a one-line takeaway and its source file.
4. **Statistics.** Every table, with source files.
5. **The agent experiment.**
   - Design: arms, emphases, repetitions, budgets, models from the logs.
   - Proposals and validity rates, admitted migration reports, judge-usable labels.
   - Selected features and their research→test fate.
   - Human vs judge, 10/17.
   - Sonnet vs Opus.
6. **AI-interaction inventory.** For each Claude use (P1–P4 in the build, P5 the post-mortem review, P6 this iteration): purpose, model, the exact prompt file, the output file, what was right, what was wrong, and what changed. Leave the team-critique cells empty. Models come from `docs/process/project_rules.md` "AI-use facts".
7. **Claims register (`results/claims.csv`).** Every claim the report may make, with columns: `claim_id`, `sentence`, `number(s)`, `source file + row/column`, `label` (CONF / POST-HOC / FWD), `verified` (y/n). Verify each number against its file. **The report may only use claims in this register.**
8. **Known issues.** List each one with a fix or a disclosure line:
   - V2c's ETF legs cancel (both map to XLI);
   - the revised-vs-as-known data gap;
   - the overlap in the 12-month placebo;
   - the mapping dilution;
   - the power limit (about 0.6 Sharpe detectable).

**Gate 1:** every number in `claims.csv` is verified, and `results_book.pdf` compiles with no missing figures.

## Stage 2: Robustness battery for V2d (frozen before running)

The point is to find out whether the core finding holds up, not to raise the Sharpe.

1. Write `analysis/v3_spec.md` listing **exactly** the checks below. Hash it, timestamp it and commit it. Then run everything once and report every result, whatever it shows.
2. Raise `N_trials` for the deflated Sharpe by the number of new portfolio variants. Record the new count.

| ID | Check | Output |
|---|---|---|
| R1 | Components: hires only, quits only, and openings and layoffs for contrast, all signed and held like V2d | table |
| R2 | **Horizon profile**: rank IC of the V2d score at h = 1, 3, 6, 9, 12, 18, 24, with HAC t (lags h+5), for research, test and full | `fig_horizon_profile.pdf`, the thesis figure: negative or flat at 1 month, positive at 12 |
| R3 | Holding period 6, 9, 12 and 18 months (same score, same construction) | table + small bar figure |
| R4 | Sub-periods: test first half and second half, ex-pandemic (drop Mar 2020–Dec 2021), pre-2020 vs post-2020 | table |
| R5 | Costs at 0, 10, 25 and 50 bp; break-even cost | table |
| R6 | Factor alpha (FF5 + Mom + group momentum) with HAC lags = 12 for the overlap; loadings | table, and add V2d to `fig_loadings` |
| R7 | Drop one industry (13 runs): minimum, median and maximum test Sharpe; the industry contributing most | table + `fig_v2d_dropone.pdf` |
| R8 | **Tightness moderator, the original thesis**: V2d IC and Sharpe in T-rising vs T-falling months, and in V/U > 1 vs < 1 months | table + `fig_v2d_tightness.pdf` |
| R9 | Block-bootstrap 90% confidence interval for the V2d test and full Sharpe (block 12, 5,000 draws) | table |
| R11 | **Fundamental law (Grinold–Kahn, the course textbook)**: for A3, V2a and V2d, implied IR = IC × √(breadth per year) × TC. Breadth = groups × independent bets per year: 13×12 for 1-month books, about 13 for the 12-month book. TC = correlation of actual weights with score-proportional weights. Compare with the realised Sharpe | table: does the realised Sharpe match what the IC and 13 groups allow? |
| R10 | **As-known data**: if `analysis/.env` has `FRED_API_KEY`, rebuild the hires and quits panels from ALFRED vintages and rerun V2a–V2d test and full. Otherwise write "not run: no key" in the results | table |

Then:
- Write `analysis/output/v3_results.md` with every result and its reading.
- Create the figures in the house style from `docs/process/project_rules.md`.
- Update the Results Book and the claims register.

**Gate 2:** the v3 spec timestamp is earlier than the first v3 output; `run.ipynb` runs top to bottom; and the v2 result files are still byte-identical.

## Stage 3: Verdict and story (still no report text)

Add `results/VERDICT.md` (1 page) to the Results Book. It covers:

- **The final verdict on each strategy.**
- **The final one-paragraph story.**
- **What we can claim**, each item with its claim IDs.
- **What we cannot claim.**
- **The figure plan for the report:** about 10 figures, and which claim each one supports.

Rules for writing the verdict:
- **If R1–R9 weaken V2d, the story says so plainly.** A clean negative with a clear explanation is a valid result.
- **If they support it, the story leads with V2d as the thesis result.** It stays labelled post-hoc and not yet tradeable, with the forward test live.
- **V2a stays reported as the declared headline, with its weaknesses.**

## Stage 4: Report v1 (`report/main.tex`)

Write the report **only from the claims register and VERDICT.md**.

- **Rebuild `report/main.tex` on the house template (Appendix A).** It must start `\input{preamble}`, `\begin{document}`, `\MakeCover`. Remove the skeleton's old preamble and port its content. The cover carries the logo, the course (MFE 230GA – Equity Markets, Fall 2026), the instructors (Raffaele Savi and Gerald Garvey, BlackRock), the GSI (Vinicio DeSola) and all five names. The logo is used automatically if `report/figures/berkeley_mfe_logo.pdf` or `.png` exists; otherwise the typographic mark appears.
- **Template rules:**
  - no bold in body text, only in titles; use `\emph` for emphasis ("\emph{Do not implement}");
  - every caption is one finding sentence, then `\hfill` and the label pill (`\tagc`, `\tagp` or `\tagf`);
  - tables are booktabs, either full width (`tabularx` with `Y` columns) or wrapped in `threeparttable` so the caption matches the table width;
  - boxes: `keybox[Title]` for the integrity box, `promptbox{Title}` for Claude prompts, `lstlisting` for code;
  - figures at `\linewidth`, or two side by side with `subcaption`;
  - `\draftfalse` stays OFF in v1 so the remaining `\todo`/`\prov` marks stay visible. Follow `ITERATION_PROMPT.md` Part 4 for structure, and `docs/process/project_rules.md` for style, labels, figures and page budget.

- **Title page:** all five names.
- **Executive summary:** at most 230 words. It covers "Do not implement", why, what survives (V2d / the thesis result, honestly sized), the forward test, and one line on Claude.
- **Replace every outdated skeleton number.** The wrong ones are: W "IC +0.04 both periods", "Sharpe ≈0.25", industry momentum +0.034, tightness split 132/141.
- **Section 3c:**
  - the fundamental-law reading (R11): what the IC and 13 groups allow, and why a modest Sharpe is the expected ceiling;
  - why the preregistered design failed;
  - then the v2 variants (all four);
  - then the V2d robustness battery;
  - then the forward test and the Q4 2026 book.
  - Note that V2c's tradable book has 4 legs because two of its positions share an ETF.
- **Section 3d:** the AI-interaction table from Stage 1, with critique cells as `\todo{critique: <name>}` spread across all five members. Then the agent experiment and the reflection.
- **Tables:** use `\footnotesize` wherever a table overflows (`v2_results.tex` is 21pt too wide).
- **Build:** zero errors, zero undefined references, no overfull box above 5pt. Render every page to PNG, look at it and fix the layout.

## Stage 5: Independent review

1. **Spawn a fresh subagent** that has not seen your work. Give it `FinalProject.pdf`, `report/main.pdf`, `report/main.tex` and `results/claims.csv`.
2. **Its tasks:**
   - grade the report against the rubric (Thesis 40, Execution 40, Originality 20);
   - trace 20 random numbers to their source files;
   - flag anything post-hoc that reads as confirmatory, any jargon, and anything that sounds AI-written;
   - list the top 10 fixes.
3. **Apply every fix that needs no human input.** Rebuild, look at the pages again, and repeat the review once.
4. **Write `report/REVIEW.md`**: both rounds, scores, fixes applied and fixes left.

## Stage 6: Morning brief

Write `MORNING_BRIEF.md` at the project root, at most one page:
- the verdict in 3 lines;
- the scoreboard;
- what changed overnight;
- the five best figures (file names);
- every remaining `\todo` with its owner:
  - Al: the AI table and reflection;
  - Elouan: references and the data appendix;
  - Alex: the "6 astra" disclosure and the integrity box;
  - everyone: critique lines;
  - Romain: final prose.
- open risks;
- how to build the report on Overleaf.

Also fix `FINDINGS_AND_PROPOSAL.md`: replace the "OpenAI Codex" guess with "engineering assistant: to be confirmed by Alex".

Commit everything.

---

## Appendix A: House LaTeX template (`report/preamble.tex`, already in the folder)

Use this file as is for both `report/main.tex` and `results/results_book.tex`. Do not change the design. Change content only through the `REPORT INFO` macros. If a package is missing on this machine, install it or drop that one line; never redesign.

Usage:

```latex
\input{preamble}
\begin{document}
\MakeCover
\section{Executive summary}
...
\bibliographystyle{plainnat}
\bibliography{refs}
\clearpage
\appendix
...
\end{document}
```

Full preamble:

```latex
% =====================================================================
%  House LaTeX template: minimal, light (Piero). Shared by report/ and results/.
% =====================================================================
\documentclass[11pt]{article}

% ---------- PAGE ----------
\usepackage[a4paper,margin=2.1cm,headheight=14pt,footskip=26pt]{geometry}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.55em}
\IfFileExists{lmodern.sty}{\usepackage[T1]{fontenc}\usepackage{lmodern}}{}
\usepackage{microtype}
\usepackage{amsmath,amssymb}
\linespread{1.04}

% ---------- COLOURS (Berkeley) ----------
\usepackage[dvipsnames]{xcolor}
\definecolor{bblue}{HTML}{003262}   % Berkeley Blue
\definecolor{bgold}{HTML}{FDB515}   % California Gold
\definecolor{ink}{HTML}{16181D}
\definecolor{mute}{HTML}{6B7280}
\definecolor{hair}{HTML}{D4D8DE}
\definecolor{paper}{HTML}{F5F6F8}
\definecolor{confc}{HTML}{003262}   % confirmatory
\definecolor{posthc}{HTML}{B35C00}  % post-hoc
\definecolor{fwdc}{HTML}{2E7D32}    % forward test
\color{ink}

% ---------- PACKAGES ----------
\usepackage{graphicx}
\usepackage{booktabs,tabularx,array,threeparttable,multirow}
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
\setlength{\aboverulesep}{0.3ex}\setlength{\belowrulesep}{0.5ex}
\usepackage{float}
\usepackage[font=small,labelfont={color=bblue,sc},labelsep=period,skip=5pt,justification=raggedright,singlelinecheck=false]{caption}
\usepackage{subcaption}
\usepackage[shortlabels]{enumitem}
\setlist{itemsep=1pt,topsep=2pt,parsep=0pt}
\usepackage{titlesec}
\usepackage{fancyhdr}
\usepackage[most]{tcolorbox}
\usepackage{listings}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning,calc}
\usepackage[round,authoryear]{natbib}
\usepackage[colorlinks=true,linkcolor=bblue,citecolor=bblue,urlcolor=bblue]{hyperref}
\usepackage[capitalise,noabbrev]{cleveref}

% ---------- REPORT INFO ----------
\newcommand{\ReportTitle}{Follow the Workers}
\newcommand{\ReportSubtitle}{Do labor-market flows predict which U.S.\ industries outperform?}
\newcommand{\CourseName}{MFE 230GA \textendash{} Equity Markets}
\newcommand{\CourseShort}{MFE 230GA}
\newcommand{\Term}{Fall 2026}
\newcommand{\SubmitDate}{October 4, 2026}

% ---------- SECTIONS (bold only in titles) ----------
\titleformat{\section}{\large\bfseries\color{bblue}}{\thesection}{0.7em}{}[{\color{hair}\titlerule[0.5pt]}]
\titlespacing*{\section}{0pt}{16pt}{8pt}
\titleformat{\subsection}{\normalsize\bfseries}{\textcolor{bblue}{\thesubsection}}{0.7em}{}
\titlespacing*{\subsection}{0pt}{11pt}{3pt}
\titleformat{\paragraph}[runin]{\normalsize\itshape}{}{}{}[.]
\titlespacing*{\paragraph}{0pt}{6pt}{0.6em}

% ---------- HEADER / FOOTER ----------
\pagestyle{fancy}\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0.4pt}
\renewcommand{\footrule}{{\color{hair}\hrule width\headwidth height\footrulewidth\vskip\footruleskip}}
\fancyhead[R]{\footnotesize\color{mute}Page \thepage}
\fancyfoot[L]{\footnotesize\color{mute}\CourseShort{} \textperiodcentered{} Final Project}
\fancyfoot[R]{\footnotesize\color{mute}\ReportTitle}

% ---------- LABELS, DRAFT MARKS ----------
\newif\ifdraft \drafttrue   % \draftfalse for the submission build
\DeclareRobustCommand{\pill}[2]{\tcbox[on line,colback=#1!9,colframe=#1!9,boxrule=0pt,arc=1.6pt,
  left=2.5pt,right=2.5pt,top=0.5pt,bottom=0.5pt,boxsep=0pt]{\textcolor{#1}{\scriptsize\textsc{#2}}}}
\DeclareRobustCommand{\tagc}{\pill{confc}{confirmatory}}
\DeclareRobustCommand{\tagp}{\pill{posthc}{post-hoc}}
\DeclareRobustCommand{\tagf}{\pill{fwdc}{forward test}}
\newcommand{\prov}[1]{\ifdraft{\setlength{\fboxsep}{1pt}\colorbox{bgold!30}{#1}}\else #1\fi}
\newcommand{\todo}[1]{\ifdraft{\color{red!70!black}\footnotesize[TODO: #1]}\fi}

% ---------- BOXES ----------
\newtcolorbox{keybox}[1][]{enhanced,breakable,sharp corners,frame hidden,boxrule=0pt,
  colback=paper,borderline west={2pt}{0pt}{bgold},left=9pt,right=9pt,top=5pt,bottom=6pt,
  fontupper=\small,before upper={\ifx\relax#1\relax\else{\textcolor{bblue}{\textsc{#1}}\par\smallskip}\fi}}
\newtcolorbox{promptbox}[1]{enhanced,breakable,sharp corners,frame hidden,boxrule=0pt,
  colback=paper,borderline west={2pt}{0pt}{bblue},left=9pt,right=9pt,top=5pt,bottom=6pt,
  before upper={{\small\textcolor{bblue}{\textsc{#1}}}\par\smallskip\raggedright\footnotesize\ttfamily}}

% ---------- CODE ----------
\lstset{language=Python,basicstyle=\ttfamily\footnotesize,columns=fullflexible,keepspaces,
  breaklines,showstringspaces=false,frame=leftline,framerule=2pt,rulecolor=\color{bblue},
  backgroundcolor=\color{paper},xleftmargin=8pt,framexleftmargin=8pt,aboveskip=6pt,belowskip=6pt,
  keywordstyle=\color{bblue},commentstyle=\color{mute}\itshape,stringstyle=\color{posthc}}

% ---------- COVER ----------
\newcommand{\BerkeleyMark}{%
  \IfFileExists{figures/berkeley_mfe_logo.pdf}{\includegraphics[height=1.4cm]{figures/berkeley_mfe_logo.pdf}}{%
  \IfFileExists{figures/berkeley_mfe_logo.png}{\includegraphics[height=1.4cm]{figures/berkeley_mfe_logo.png}}{%
  {\color{bblue}\fontsize{24}{26}\selectfont\bfseries Berkeley}\hspace{0.7em}%
  {\color{bgold}\rule[-3pt]{1.4pt}{22pt}}\hspace{0.7em}%
  \parbox[b]{7cm}{\color{bblue}\footnotesize\textsc{Haas School of Business}\\[-1pt]\textsc{Master of Financial Engineering}}}}}

\newcommand{\MakeCover}{%
\begin{titlepage}
\newgeometry{margin=2.5cm}
\BerkeleyMark
\vspace*{0.26\textheight}

{\raggedright
{\color{mute}\small\textsc{\CourseShort{} \textperiodcentered{} Final Project \textperiodcentered{} \Term}}\par\vspace{10pt}
{\fontsize{34}{38}\selectfont\bfseries\color{bblue}\ReportTitle\par}
\vspace{10pt}
{\Large\color{mute}\ReportSubtitle\par}
\vspace{18pt}
{\color{bgold}\rule{3.2cm}{1.6pt}}\par}

\vfill
\begin{minipage}[t]{0.46\textwidth}
{\color{mute}\footnotesize\textsc{Team}}\par\vspace{4pt}
\begin{tabular}{@{}l l@{}}
Romain   & \textsc{Almeida} \\
Elouan   & \textsc{Bahri} \\
Al Yazid & \textsc{Bensaid} \\
Piero    & \textsc{Pelosi} \\
Alex     & \textsc{Roesler}
\end{tabular}
\end{minipage}\hfill
\begin{minipage}[t]{0.46\textwidth}
{\color{mute}\footnotesize\textsc{Course}}\par\vspace{4pt}
\CourseName\par\vspace{8pt}
{\color{mute}\footnotesize\textsc{Instructors}}\par\vspace{4pt}
Raffaele Savi and Gerald Garvey\par{\small\color{mute}BlackRock}\par\vspace{8pt}
{\color{mute}\footnotesize\textsc{Graduate Student Instructor}}\par\vspace{4pt}
Vinicio DeSola
\end{minipage}

\vspace{1.4cm}
{\color{hair}\rule{\textwidth}{0.5pt}}\par\vspace{2pt}
{\footnotesize\color{mute}UC Berkeley Haas \textperiodcentered{} Master of Financial Engineering\hfill\SubmitDate}
\restoregeometry
\end{titlepage}
\setcounter{page}{1}}
```
