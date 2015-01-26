
import collections

# Markers for indicating start and stop of sentences
SENTENCE_START_STRING = "<<START>>"
SENTENCE_END_STRING = "<<END>>"

# Rebuilds a set of words into a single string.
# Takes parts[start: start + length] and combines into a single string 
# with spaces.
def build_gram(parts, start, length):
	ret_str = ""
	for i in xrange(start, start + length):
		ret_str = ret_str + parts[i] + ' '
	return ret_str[:-1] # don't include trailing space.

# Adds a single line to the model.
def add_line_to_model(sentence, model):
	parts = sentence.split(' ')
	parts.insert(0, SENTENCE_START_STRING)
	parts.insert(len(parts), SENTENCE_END_STRING)

	for i in xrange(len(parts) - 1):
		for m_idx in xrange(len(model)):
			if (i + m_idx + 1 < len(parts)):
				g = build_gram(parts, i, m_idx + 1)
				add_gram_to_model(g, parts[i+1], model[m_idx])

# Adds a single gram pair to the model.
def add_gram_to_model(g1, g2, model):
	d = model[g1]
	if (g2 in d):
		d[g2] += 1
	else:
		d[g2] = 1

# Takes in the word counts model (counts) and generates a probabiliites model.
def build_probabilities_from_counts(counts, model):
	for g1, g1_out in counts.items():
		total_counts = float(sum(g1_out.values()))
		for g2, g2_count in g1_out.items():
			model[g1][g2] = g2_count / total_counts
		if sum(model[g1].values()) < 0.99 or sum(model[g1].values()) > 1.01:
			print "ERROR: " + sum(model[g1].values())

# Generates a probability model from the given corpus.
def build_model(filename):
	f = open(filename)
	# {prefix1 : {suffix1: count1, suffix2:count2} ... }
	m = [collections.defaultdict(dict), # n = 1
		 collections.defaultdict(dict), # n = 2
		 collections.defaultdict(dict)] # n = 3
	for line in f:
		add_line_to_model(line.lower(), m)

	m_2 = [collections.defaultdict(dict), # n = 1
		   collections.defaultdict(dict), # n = 2
		   collections.defaultdict(dict)] # n = 3
	print "building p tables"
	for i in xrange(len(m)):
		build_probabilities_from_counts(m[i], m_2[i])
	return m_2
