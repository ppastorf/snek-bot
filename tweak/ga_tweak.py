# CONSTANTS FOR THE GENETIC ALGORITHM #

'''
	this constants are the only thing that need be changed to experiment with
	different evolutions scenarios, with exception to the number of genes, of course.
'''

# Size of each population
POP_SIZE = 100

# Number of individuals from each generation to be selected for breeding (progenitors)
N_PROG = 10

# These values should follow the rule POP_SIZE = N_PROG * 10*N_BATCH, for every integer N_BATCH

# Every pair of parents should result in 10*N_BATCH chromosomes, as every crossover
# iteration generates 10 chromosomes (thisis arbitrary)
N_BATCH = int( (POP_SIZE/N_PROG)/10 )

# Number of lucky chromosomes to be randomly selected for breeding,
# to maintain genetic variability
LUCKY_ONES = 0

# Number of generations
N_GEN = 20

# Mutation rate
MUT_RATE = 0.1

# Number of genes (this can't be tweaked without making other changes to the code)
N_GENES = 5

# Breeding method (either 'genetic', 'arithmetic', 'coinflip' or 'mixed')
BREEDING = 'genetic'

# GENE BOUNDS #

'''
	This are the lower (first value) and upper (second value) boundaries for the random
	generation of genes, wich happens in the inicialization of the first generation
	and in the event of mutation.
'''

GENE1 = [20.000, 200.000]
GENE2 = [01.000, 10.000]
GENE3 = [1.0000, 2.0000]
GENE4 = [0.0010, 0.0020]
GENE5 = [-1.000, 01.000]