# LaTeX
## Setup
### LaTeX
```sh
sudo apt install texlive-full
```
## Usage
### Build
```sh
latexmk thesis.tex -bibtex -pdf -quiet -f
```
### Clean
```sh
latexmk -CA
```
### View
```sh
open thesis.pdf
```
