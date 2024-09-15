from heredity import *


people = load_data("data/family1.csv")
one_genes = {"Molly"}
two_genes = {"Arthur"}
have_trait = {"Ron"}





answer = joint_probability(people, one_genes, two_genes, have_trait)

print(answer)