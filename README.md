# RicoSLAM: Localization and Mapping in Dynamic Environments

PhD Thesis of [Ricardo B. Sousa](https://sousarbarb.github.io/), submitted to
the [Faculty of Engineering, University of Porto (FEUP)](https://sigarra.up.pt/feup/en/)
in the scope of the
[Doctoral Program in Electrical and Computer Engineering (PDEEC)](https://sigarra.up.pt/feup/en/CUR_GERAL.CUR_VIEW?pv_curso_id=682).
The thesis was developed at
[CRIIS - Centre for Robotics in Industry and Intelligent Systems](https://www.inesctec.pt/en/centres/criis)
of [INESC TEC](https://www.inesctec.pt/en/), within
[iiLab - industry and innovation Laboratory](https://www.inesctec.pt/en/laboratories/iilab-industry-and-innovation-lab).
The PhD journey included a visiting research period with
[Prof. Dr. Giorgio Grisetti](https://sites.google.com/dis.uniroma1.it/grisetti)
at the [Robots Vision and Perception (RVP)](https://rvp-group.net/) research
group from the
[Department of Computer, Control, and Management Engineering Antonio Ruberti (DIAG)](https://www.diag.uniroma1.it/en)
of [Sapienza University of Rome](https://www.uniroma1.it/en).

This repository contains the LaTeX sources of the PhD Thesis document,
the data and configuration files used throughout it,
the latest version of the document ([`thesis.pdf`](thesis.pdf)), and
complementary material such as the Thesis Research Proposal (TRP),
reference examples of previous theses at FEUP, and earlier
revisions produced over the course of the doctorate.

The main scientific contribution of the thesis is the **RicoSLAM framework**
([github](https://github.com/INESCTEC/ricoslam)),
a Simultaneous Localization and Mapping (SLAM) system for
dynamic industrial environments built around a distance map-based tracking
front-end, a factor graph optimization back-end using the
[srrg2_solver](https://gitlab.com/srrg-software/srrg2_solver) framework,
online and offline dynamics filtering through ray tracing, and a novel distance
map-based global bundle adjustment formulation.
The front-end tracker supports the distance map-based registration formulations
proposed in the PhD Thesis and also Iterative Closest Point (ICP) with
distance map-guided data association.
RicoSLAM has been deployed on-site across six industrial companies in the
scope of the GreenAuto and related projects.

## Author

- **Ricardo B. Sousa**
  ([ricardo.b.sousa@inesctec.pt](mailto:ricardo.b.sousa@inesctec.pt))
  ([github](https://github.com/sousarbarb/),
  [gitlab](https://gitlab.com/sousarbarb/),
  [orcid](https://orcid.org/0000-0003-4537-5095),
  [website](https://sousarbarb.github.io/),
  [youtube](https://www.youtube.com/channel/UCXTR8mMlG0VOC_06PKg5KBQ))

## Supervisors

- **Prof. Dr. António Paulo Moreira**
  ([amoreira@fe.up.pt](mailto:amoreira@fe.up.pt))
  ([orcid](https://orcid.org/0000-0001-8573-3147))
- **Héber Miguel Sobreira, PhD**
  ([heber.m.sobreira@inesctec.pt](mailto:heber.m.sobreira@inesctec.pt))
  ([orcid](https://orcid.org/0000-0002-8055-1093))

## Visiting Research Period

- **Period:** February - July 2024 (6 months)
- **Host Institution:**
  [Department of Computer, Control, and Management Engineering Antonio Ruberti (DIAG)](https://www.diag.uniroma1.it/en),
  [Sapienza University of Rome](https://www.uniroma1.it/en) (Rome, Italy)
- **Host Supervisor:** **Prof. Dr. Giorgio Grisetti**
  ([grisetti@diag.uniroma1.it](mailto:grisetti@diag.uniroma1.it))
  ([google-scholar](https://scholar.google.com/citations?user=yD-SFG4AAAAJ))

## Repository Structure

```
phd-thesis/
├── .vscode/    # Visual Studio Code settings (Code Spell Checker)
├── cover/      # Cover PDF and instructions to merge it with thesis.pdf
├── data/       # Configuration files and data (when small enough) used in the thesis
├── doc/        # Thesis Research Proposal (TRP) and related documentation
├── examples/   # Reference examples of PhD theses at FEUP
├── latex/      # LaTeX project sources (build offline with latexmk)
├── versions/   # Thesis PDF versions produced throughout the doctorate
└── thesis.pdf  # Latest version of the PhD Thesis
```

## Build

### Dependencies
```sh
sudo apt-get install -y texlive-full latexmk biber
```

### Compile
```sh
cd latex/
latexmk -bibtex -pdf -f thesis.tex
```

### Clean
```sh
latexmk -c  # clean up (remove) all nonessential files, except dvi|ps|pdf files
latexmk -C  # clean up (remove) all nonessential files, including dvi|ps|pdf files
```

### Merging the Cover

See [`cover/README.md`](cover/README.md) for the procedure to merge the
exported cover PDF with the body produced from `latex/` into the final
`thesis.pdf`.

## Data and Code

Datasets, evaluation outputs, and supporting code associated with the thesis
are published in dedicated, citable archives rather than stored directly in
this repository:
- **Datasets and evaluation outputs:** Zenodo _(DOI to be added upon
  deposit)_
- **IILABS 3D dataset:**
  [iilabs3d-toolkit](https://github.com/jorgedfr/iilabs3d-toolkit)
  _(IEEE Access 2025)_
- **RicoSLAM framework source code:**
  [ricoslam](https://github.com/INESCTEC/ricoslam)
  _(to be open-sourced, GitHub-archived release on Zenodo, DOI to be added)_

## License

Distributed under the GNU AGPLv3 license. See `LICENSE` for more information.

## Citation

If you use material from this thesis in a work that leads to a scientific
publication, please consider citing it as follows.

**Plain Text**

R.B. Sousa,
"RicoSLAM: Localization and Mapping in Dynamic Environments,"
PhD Thesis, Faculty of Engineering, University of Porto, Porto, Portugal,
2026.

**BibTeX**

```bibtex
@PHDTHESIS{sousa2026thesis,
  author  = {Ricardo B. Sousa},
  title   = {{RicoSLAM}: Localization and Mapping in Dynamic Environments},
  school  = {Faculty of Engineering, University of Porto},
  address = {Porto, Portugal},
  year    = {2026},
  type    = {{PhD} Thesis}}
```

## Contacts

If you have any questions or you want to know more about this work, please
contact:
- **Ricardo B. Sousa**
  ([ricardo.b.sousa@inesctec.pt](mailto:ricardo.b.sousa@inesctec.pt))
  _(Corresponding Author)_
  ([github](https://github.com/sousarbarb/),
  [gitlab](https://gitlab.com/sousarbarb/),
  [orcid](https://orcid.org/0000-0003-4537-5095),
  [website](https://sousarbarb.github.io/),
  [youtube](https://www.youtube.com/channel/UCXTR8mMlG0VOC_06PKg5KBQ))
- **Héber Miguel Sobreira, PhD**
  ([heber.m.sobreira@inesctec.pt](mailto:heber.m.sobreira@inesctec.pt))
  ([orcid](https://orcid.org/0000-0002-8055-1093))
- **Prof. Dr. António Paulo Moreira**
  ([amoreira@fe.up.pt](mailto:amoreira@fe.up.pt))
  ([orcid](https://orcid.org/0000-0001-8573-3147))
- **Prof. Dr. Giorgio Grisetti**
  ([grisetti@diag.uniroma1.it](mailto:grisetti@diag.uniroma1.it))
  ([github](https://github.com/grisetti),
  [gitlab](https://gitlab.com/grisetti),
  [google-scholar](https://scholar.google.com/citations?user=yD-SFG4AAAAJ))

## Acknowledgements

- [5dpo Robotics Team](https://5dpo.github.io/)
- [CRIIS - Centre for Robotics in Industry and Intelligent Systems](https://www.inesctec.pt/en/centres/criis),
  [INESC TEC - Institute for Systems and Computer Engineering, Technology and Science](https://www.inesctec.pt/en/)
- [Faculty of Engineering, University of Porto (FEUP)](https://sigarra.up.pt/feup/en/)
- [Flowbotic Mobile Systems, Lda](https://www.flowbotic.eu/)
- [Robots Vision and Perception (RVP)](https://rvp-group.net/) research group
  from the
  [Department of Computer, Control, and Management Engineering Antonio Ruberti (DIAG)](https://www.diag.uniroma1.it/en)
  of [Sapienza University of Rome](https://www.uniroma1.it/en)

## Funding

**FCT PhD Scholarship**

This work has received funding from National Funds through
the Portuguese funding agency,
[FCT - Fundação para a Ciência e a Tecnologia](https://www.fct.pt/en/), within
scholarship 2021.04591.BD (DOI:
[10.54499/2021.04591.BD](https://doi.org/10.54499/2021.04591.BD)).

- **Title:** RicoSLAM: long-term localization and mapping in dynamic environments
- **Reference:** 2021.04591.BD
- **DOI:** [10.54499/2021.04591.BD](https://doi.org/10.54499/2021.04591.BD)
- **Researcher:** Ricardo Barbosa Sousa
  ([orcid](https://orcid.org/0000-0003-4537-5095),
  [ciencia-vitae](https://www.cienciavitae.pt/en/D11E-2C67-1CCE))
- **Host Institutions:**
    - [Faculty of Engineering, University of Porto (FEUP)](https://sigarra.up.pt/feup/en/)
      _(main)_
    - [INESC TEC - Institute for Systems and Computer Engineering, Technology and Science](https://www.inesctec.pt/en/)
- **Funding Agency:**
  [Fundação para a Ciência e a Tecnologia (FCT)](https://www.fct.pt/en/),
  Portugal
- **Project Timeline:** September 2021 - January 2025
- **Funding Timeline:** September 2021 - March 2023

**GreenAuto: Green innovation for the Automotive Industry**

This work was co-financed by Component 5 - Capitalization and Business
Innovation, integrated in the Resilience Dimension of the Recovery and
Resilience Plan within the scope of the Recovery and Resilience Mechanism
(MRR) of the European Union (EU), framed in the Next Generation EU, for the
period 2021-2026, within project GreenAuto, with reference 54.

- **Operation Code:** 02/C05-i01.02/2022.PC644867037-00000013
- **Beneficiary:** Peugeot Citröen Automóveis Portugal, S.A.
- **Work Package:** WP10 - Automated logistics for the automotive industry
- **Product, Processes, or Services (PPS):**
  PPS18 - 3D navigation system for mobile robotic equipment
- **Consortium Partners:**
    - [Flowbotic Mobile Systems, Lda](https://www.flowbotic.eu/) _(leader)_
    - [Faculty of Engineering, University of Porto (FEUP)](https://www.up.pt/feup/en/)
    - [INESC TEC - Institute for Systems and Computer Engineering, Technology and Science](https://www.inesctec.pt/en/)
    - [STAR](https://starinstitute.pt/)
    - [Kaizen](https://kaizen.com/pt-pt/)
    - [Institute for Systems and Robotics (ISR)-Coimbra](https://www.isr.uc.pt/)
- **Timeline:** October 2021 - December 2025
- **Duration:** 51 months
- **URL:**
  [https://transparencia.gov.pt/en/fundos-europeus/prr/beneficiarios-projetos/projeto/02/C05-i01.02/2022.PC644867037-00000013/](https://transparencia.gov.pt/en/fundos-europeus/prr/beneficiarios-projetos/projeto/02/C05-i01.02/2022.PC644867037-00000013/)
