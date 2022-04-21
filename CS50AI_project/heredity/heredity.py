import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,  #USE THESE IF NO DATA GIVEN ABOUT THE PERSON'S PARENTS
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene I.E. prob'y of having hearing impairment given person has 2 copies of the gene
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

    # Mutation probability I.E. prob'y that a gene passed from a parent to child mutates, meaning it changes from the problematic gene to another type or vice versa.
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
    class People():
        def __init__(self,name):
            self.name = name
            self.trait = people[self.name]["trait"]

        def m_gene(self):
            if people[self.name]["mother"] in zero_genes:
                return 0
            elif people[self.name]["mother"] in one_gene:
                return 1
            else:
                return 2

        def f_gene(self):
            if people[self.name]["father"] in zero_genes:
                return 0
            elif people[self.name]["father"] in one_gene:
                return 1
            else:
                return 2


    people_set = set([person for person in people])
    zero_genes = people_set - one_gene - two_genes #this is set of people that will not have the gene
    zeros = [People(person) for person in zero_genes]
    ones = [People(person) for person in one_gene] #these are lists of people assigned to a set no. of genes, objects are of class People created above
    twos = [People(person) for person in two_genes]

    m = PROBS["mutation"]
    p = 1  #p here will be the the joint probability of the things stated above

    for person in zeros:
        if people[person.name]["mother"] == None:
            p *= PROBS["gene"][0]
        else: #the case that we know who the mother and father of this person are
            if person.m_gene() == person.f_gene() == 0:
                p *= (1 - m)**2
            elif person.m_gene() + person.f_gene() == 1:
                p *= (1 - m) * 0.5 
            elif person.m_gene() == person.f_gene() == 1:
                p *= 0.5**2
            elif person.m_gene() + person.f_gene() == 2: #if either the mum or dad has 2 genes and the other 0 genes
                p *= m * (1-m)
            elif person.m_gene() + person.f_gene() == 3:
                p *= m * 0.5
            else:
                p *= m**2

        if person.name in have_trait:
            p *= PROBS["trait"][0][True]
        else:
            p *= PROBS["trait"][0][False]


    for person in ones:
        if people[person.name]["mother"] == None:
            p *= PROBS["gene"][1]

        else: #the case that we know who the mother and father of this person are
            if person.m_gene() == person.f_gene() == 0:
                p *= 2*(1 - m)*m
            elif person.m_gene() + person.f_gene() == 1:
                p *= 0.5*(1-m) + (0.5*m)
            elif person.m_gene() == person.f_gene() == 1:
                p *= 2 * 0.5**2
            elif person.m_gene() + person.f_gene() == 2: #if either the mum or dad has 2 genes and the other 0 genes
                p *= m**2 + (1-m)**2
            elif person.m_gene() + person.f_gene() == 3:
                p *= (1-m)*0.5 + m*0.5
            else:
                p *= 2*m*(1-m)

        if person.name in have_trait:
            p *= PROBS["trait"][1][True]
        else:
            p *= PROBS["trait"][1][False]



    for person in twos:
        if people[person.name]["mother"] == None:
            p *= PROBS["gene"][2]

        else: #the case that we know who the mother and father of this person are
            if person.m_gene() == person.f_gene() == 0:
                p *= m**2
            elif person.m_gene() + person.f_gene() == 1:
                p *= 0.5*m
            elif person.m_gene() == person.f_gene() == 1:
                p *= 0.5**2
            elif person.m_gene() + person.f_gene() == 2: #if either the mum or dad has 2 genes and the other 0 genes
                p *= (1-m)*m
            elif person.m_gene() + person.f_gene() == 3:
                p *= (1-m)*0.5
            else:
                p *= (1-m)**2

        if person.name in have_trait:
            p *= PROBS["trait"][2][True]
        else:
            p *= PROBS["trait"][2][False]


    return p





def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    people_set = set([person for person in probabilities])
    zero_genes = people_set - one_gene - two_genes
    for person in zero_genes:
        probabilities[person]["gene"][0] += p
    for person in one_gene:
        probabilities[person]["gene"][1] += p
    for person in two_genes:
        probabilities[person]["gene"][2] += p


    for person in have_trait:
        probabilities[person]["trait"][True] += p
    for person in people_set - have_trait:
        probabilities[person]["trait"][False] +=p



def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in probabilities:

        original_gene_probs = list(probabilities[person]["gene"].values())
        original_gene_total = sum(original_gene_probs)
        gene_multiplier = 1/original_gene_total

        for num in probabilities[person]["gene"]:
            probabilities[person]["gene"][num] *= gene_multiplier


        original_trait_probs = list(probabilities[person]["trait"].values())
        original_trait_total = sum(original_trait_probs)
        trait_multiplier = 1/original_trait_total

        for t in probabilities[person]["trait"]:
            probabilities[person]["trait"][t] *= trait_multiplier


if __name__ == "__main__":
    main()
