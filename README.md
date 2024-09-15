# Genomic Inheirtance Model

## Overview

This project utilizes Bayesian Networks to make inferences about a population's gene probabilities and trait exhibition. Given information about individuals, their parents, and observable traits (e.g., hearing loss) caused by a specific gene, our AI infers:

1. Probability distributions for each person's genes
2. Probability distributions for trait exhibition in any person
## Background

Hearing impairment affects millions of newborns worldwide, with mutated versions of the GJB2 gene being a leading cause. This project explores the probabilistic relationships between GJB2 gene inheritance and hearing impairment, shedding light on the complex interactions between genetic and environmental factors. This project simulates the inheritance patterns of the GJB2 gene, accounting for:

- Probabilistic gene transmission from parents to offspring
- Potential gene mutations after transmission

## Project Goals

This Heredity project implements a Bayesian Network to:

1. Model gene inheritance patterns
2. Infer gene probability distributions for each person
3. Calculate trait exhibition probabilities for any person

## Implementation

This project utilizes [programming language/framework] to:

1. Construct a Bayesian Network representing gene inheritance and trait relationships
2. Perform probabilistic inference to calculate gene and trait probabilities

## Input Data

The project expects input data in a CSV file with the following format:

| Name    | Mother | Father | Trait |
| ------- | ------ | ------ | ----- |
| Arthur  |        |        | 0     |
| Charlie | Molly  | Arthur | 0     |
| Fred    | Molly  | Arthur | 1     |
| Ginny   | Molly  | Arthur |       |
| Molly   |        |        | 0     |
| Ron     | Molly  | Arthur |       |

Where:

- Name: Unique identifier for each individual
- Mother and Father: Parents' names (leave blank if unknown)
- Trait: Observable trait (0 = absent, 1 = present)

Please ensure the input CSV file is formatted correctly to ensure accurate results.

## Output

The project outputs:

1. Gene probability distributions for each person
2. Trait exhibition probability distributions for any person

This happens in the following format - 

Person: 
  Gene: 
    2: probability of having 2 copies of the gene
    1: probability of having 1 copy of the gene
    0: probability of having 0 copies of the gene
  Trait: 
    True: probability of exhibiting the trait
    False: probability of not exhibiting the trait

## Usage

To run the project, execute the following command:
```
python heredity.py data/filename.csv
```

