# llm_table_transform

## Overview

A script that takes two CSV format tables A and B, and reformats table B to have the same column names and data-formatting as table A. 

Uses OpenAI API + GPT-4 with a LangChain interface.

## Usage

1. Go to main directory, create new conda environment using yaml provided: ```conda env create -f llm_transform_env.yml```
2. Once environment created, activate: ```conda activate llm_env```
3. Go to ```main.py``` and ensure your openAI API key is correct.
4. Run the main script, with following arguments: ```python main.py <path to table A> <path to table B> <desired name of saved table.csv>```

The script should guide you through transformation of the table. 

Example usage:

```python main.py tables/template.csv tables/table_A.csv table_a_transformed.csv```

This will compare `Table_A.csv` to a table called `template.csv` and reformat data and column names from A to those of template.


