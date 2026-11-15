# FIN42330 Group Project

## Project structure

```
Group Assignment/
├── Data on Assets/          # Data files (NOT in git, add them locally)
├── Section A/
│   ├── auxiliary_functions.py                           # All functions live here
│   └── Return_Forecasting_and_Portfolio_Allocation.ipynb # Calls functions, shows results
└── Section B/               # Streamlit website
```

> `.xlsx`, `.pdf` and `.docx` files are ignored by git. Download them from Brightspace and put them in `Data on Assets/` with the exact file names above.

## How Section A works

- **Functions go in `auxiliary_functions.py`**, each one with a docstring.
- **The notebook only calls them**, then shows tables, figures and discussion.
- The notebook imports the module like this (first cell):

```python
%load_ext autoreload
%autoreload 2
import auxiliary_functions as af

excess = af.compute_excess_returns(prices, rf)
```

- `autoreload` picks up edits to the `.py` file without restarting the kernel.
- Use the **Anaconda** Python interpreter/kernel (it has numpy, pandas, etc.).

## Git workflow

> ⚠️ **Do NOT work on `main`.** Only the repo owner merges into `main`.

```bash
git clone https://github.com/aboytech/Portfolio_Analyzer.git   # first time only
git checkout main && git pull                  # get the latest version
git checkout -b yourname/task                  # e.g. maria/a3-predictors
# ...work...
git add <files>
git commit -m "Short description of the change"
git push -u origin yourname/task
```

Then open a **Pull Request** on GitHub into `main`. Before starting new work, pull `main` again and create a new branch.

Git cheat sheet: https://education.github.com/git-cheat-sheet-education.pdf
