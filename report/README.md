# ESPRIM Final-Year Project LaTeX Template - ASIIN / EUR-ACE

This folder contains a LaTeX template for final-year engineering reports, compatible with Overleaf and structured according to the kind of academic reading expected in demanding quality and accreditation contexts.

## Purpose

The template is designed to help students produce a report that is:
- well structured,
- scientifically argued,
- aligned with the institutional framework,
- readable for both academic and professional juries,
- coherent with expectations inspired by ASIIN / EUR-ACE reviews.

## Template contents

- `main.tex`: main file.
- `config.tex`: all editable information (name, title, discipline, supervisors, etc.).
- `sections/`: front matter, integrated institutional guide, introduction, conclusion.
- `chapters/`: 5 compulsory chapters.
- `annexes/`: recommended matrices, AI/reproducibility guide, final checklist.
- `references.bib`: example bibliography with reusable BibTeX entries.
- `assets/logo-esprim.png`: official logo integrated into the cover page.

## Guide mode and clean submission mode

In `config.tex`:
- `\showguidetrue`: displays guidance boxes.
- `\showguidefalse`: hides the guidance for the final submission version.

## Target disciplines

The template is intended for three broad families of topics:
- Data Science / AI
- EET (Embedded Electronics and Telecommunications)
- Mechatronics

In `config.tex`, adjust:
- `\DisciplineName`
- `\disciplinecode` with one of the following values:
  - `ds`
  - `eet`
  - `meca`

## How to use on Overleaf

1. Create a new Overleaf project.
2. Upload the full ZIP content.
3. Open `main.tex`.
4. Compile with **pdfLaTeX**.
5. Edit `config.tex` and progressively replace every `\todo{...}`.

## Integrated guide section

The template includes an institutional guide visible in guide mode. It contains:
- objectives of the final-year internship/project,
- recommended evaluation criteria,
- traceability expectations,
- bibliographic instructions,
- IEEE reference examples,
- BibTeX examples that can be copied and adapted,
- the recommended minimum for master/engineering degree level: **25 references**, with a majority of indexed sources.

## Good practices

- Keep a sober and professional style.
- Prefer readable figures and synthetic tables.
- Avoid long uncommented code blocks.
- Justify technical choices.
- Discuss limitations, not only successes.
- Declare the use of generative AI if applicable.

## Important note

This template is intentionally pedagogical. It combines:
- a report structure,
- integrated writing instructions,
- an institutional reading guide,
- traceability table models,
- a final control checklist.

For the official submission, remember to disable guide mode.
