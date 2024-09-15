import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    """
    Joint probability is basically AND. AND of probabs is to be calculated.
    """
    no_genes = []
    no_trait = []
    final_prob = 1
    for person in people:
        if people[person]["name"] not in one_gene and people[person]["name"] not in two_genes:
            no_genes.append(people[person]["name"])

        if people[person]["name"] not in have_trait:
            no_trait.append(people[person]["name"])


    for person in people:


        if people[person]["name"] in one_gene:
            if people[person]["father"] == None and people[person]["mother"] == None:
                gene_prob = PROBS["gene"][1]            
            else:
                father = people[person]["father"]
                mother = people[person]["mother"]

                # if father = 0 and mother = 0
                if father in no_genes and mother in no_genes:
                    gene_prob = (1-PROBS["mutation"])*(PROBS["mutation"]) + (1-PROBS["mutation"])*(PROBS["mutation"])
                
                elif ((father in one_gene or father in two_genes) and mother in no_genes) or ((mother in one_gene or mother in two_genes) and father in no_genes):
                # if one parent has one or two genes, and other has 0
                    gene_prob = PROBS["mutation"]*PROBS["mutation"] + (1-PROBS["mutation"])*(1-PROBS["mutation"])

                elif (father in one_gene or father in two_genes) and (mother in one_gene or mother in two_genes):
                    gene_prob = PROBS["mutation"]*(1-PROBS["mutation"]) + PROBS["mutation"]*(1-PROBS["mutation"])
            
            if people[person]["name"] in have_trait:
                person_prob = gene_prob * PROBS["trait"][1][True]
            
            else:
                person_prob = gene_prob * PROBS["trait"][1][False]

        # two gene mfs
        elif people[person]["name"] in two_genes:

            if people[person]["father"] == None and people[person]["mother"] == None:
                gene_prob = PROBS["gene"][2]

            else: 
                father = people[person]["father"]
                mother = people[person]["mother"]

                if father in no_genes and mother in no_genes:
                    gene_prob  = PROBS["mutation"]*PROBS["mutation"]

                elif ((father in one_gene or father in two_genes) and mother in no_genes) or ((mother in one_gene or mother in two_genes) and father in no_genes):
                # if one parent has 0 and one parent has 1 or two
                    gene_prob = PROBS["mutation"]*(1-PROBS["mutation"]) 

                elif (father in one_gene or father in two_genes) and (mother in one_gene or mother in two_genes):
                    gene_prob = (1-PROBS["mutation"])*(1-PROBS["mutation"])

            if people[person]["name"] in have_trait:
                person_prob = gene_prob * PROBS["trait"][2][True]
            
            else:
                person_prob = gene_prob * PROBS["trait"][2][False]


        # 0 gene mfs
        elif people[person]["name"] in no_genes:        
        
            if people[person]["father"] == None and people[person]["mother"] == None:
            # No parents
                gene_prob = PROBS["gene"][0]

            else:
                father = people[person]["father"]
                mother = people[person]["mother"]

                if father in no_genes and mother in no_genes:
                    gene_prob  = (1-PROBS["mutation"])*(1-PROBS["mutation"])
                elif ((father in one_gene or father in two_genes) and mother in no_genes) or ((mother in one_gene or mother in two_genes) and father in no_genes):
                # one with 1 or 2 genes, other with 0
                    gene_prob = PROBS["mutation"]*(1-PROBS["mutation"]) 

                elif (father in one_gene or father in two_genes) and (mother in one_gene or mother in two_genes):
                    gene_prob = PROBS["mutation"]*PROBS["mutation"]

            if people[person]["name"] in have_trait:
                person_prob = gene_prob * PROBS["trait"][0][True]

            else:
                person_prob = gene_prob * PROBS["trait"][0][False]

        final_prob = final_prob * person_prob

    return final_prob

    raise NotImplementedError


    final_prob = 1

    for person in people:

        person_prob = 1
        person_genes = (2 if person in two_genes else 1 if person in one_gene else 0)
        person_trait = person in have_trait

        father = people[person]["father"]
        mother = people[person]["mother"]

        if not mother and not father:
            person_prob = PROBS["gene"][person_genes]

        else:
            mother_prob = inherit_prob(mother, one_gene, two_genes)
            father_prob = inherit_prob(father, one_gene, two-genes)

            if person_genes == 2:
                person_prob *= mother_prob * father_prob
            elif person_genes == 1:
                person_prob *= (1-mother_prob)*(father_prob) + (1-father_prob)(mother_prob)
            else:
                person_prob *= (1-mother_prob)*(1-father_prob)
            
        person_prob *= PROBS["trait"][person_genes][person_trait]

        joint_prob *= person_prob



def inherit_prob(parent, one_gene, two_genes):

    if parent in one_gene:
        return 0.5
    elif parent in two_genes:
        return 1 - PROBS["mutation"]
    else:
        return PROBS["mutation"]



def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        gene_number = 1 if person in one_gene else 2 if person in two_genes else 0
        probabilities[person]["gene"][gene_number] += p
        probabilities[person]["trait"][person in have_trait] += p
    


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    normalized = probabilities.copy()
    for person in probabilities:
        for typ in ['gene', 'trait']:
            summed = sum(probabilities[person][typ].values())
            for category in probabilities[person][typ]:
                val = probabilities[person][typ][category]
                normalized_val = val / summed
                normalized[person][typ][category] = normalized_val
    return normalized
    raise NotImplementedError


if __name__ == "__main__":
    main()
