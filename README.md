# Italiy Population Heatmap

## Overview
This repo contains code to visualize the population in each Italian municipality in Southern Italy. The scope of this project is identifying the municipalities that offer financial incentives to move in at retirement age. Hence, it highlights Souther Italian cities with less than 20k inhabitants.

The definition of `Southern Italy` has been made ad hoc, and it includes only the regions covered in this tax incentive program.

## Features

- **Web deployment**: `GitHub Page` automatically deploys the main branch viz to [this website link](https://thegitofdaniel.github.io/italy_population_heatmap/).

## Installation

With `GitHub Codespace`, the environment should have all requirements already installed.

## Usage
### Notebooks Demos
[Please check the notebooks folder](notebooks/) for demos of how to use this package.

### Website Deployment
To generate [index.html](index.html), run:
```bash
python src/main.py
```
An automated pipeline will deploy [index.html](index.html) as a webpage at [this website link](https://thegitofdaniel.github.io/italy_population_heatmap/).

### Streamlit
```bash
streamlit run src/app.py --server.enableCORS false --server.enableXsrfProtection false
```
