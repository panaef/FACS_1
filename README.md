# FACS_1

Simple analysis of FACS data (Flojo Tables)
Start with a table of percentages (popluations columns, samples in rows),
and automatically calculate the percentages of each single poplation,
shown as % of total compartment.
Furthermore, the code creates a graph for each final column,
including statistics.

This is the version to edit.

## Getting Started

First set up your development environment.

```bash
# navigate into the project

# create projects virtual environment
python3 -m venv venv

# activate environment
source ./venv/Scripts/activate  # Windows
source ./venv/bin/activate  # Linux

# install packages
pip install -r requirements.txt
```

Now that the environment is setup edit the `./facs_analysis/config.py` file
with the correct filepaths etc. and make sure the data is available in these
paths.

```bash
# run the cli script
python ./facs_analysis/cli.py
```
