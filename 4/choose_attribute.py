import numpy as np
import pprint
from random import choice

random = False
pp = pprint.PrettyPrinter(indent=4)

def main():

    f = open("training.txt")
    examples = []
    for line in f.readlines():
      examples.append(line.rstrip("\n").split("\t"))
   
    attributes = {
      "1": [],
      "2": [],
      "3": [],
      "4": [],
      "5": [],
      "6": [],
      "7": [],
    }

#    ex = [
#        [2,2],
#        [1,1,1,1],
#        [1,1,2,2,2,2],
#    ]
#
#    parent = [1,1,1,1,1,1,2,2,2,2,2,2]
#
#    print information_gain(ex, parent)

    for i in range(len(examples)):
      for j in range(1,len(examples[i])):
        # For each attribute save the outcome if the attribute is true
        if examples[i][j] == "1":
          attributes[str(j)].append(examples[i][-1])

    print importance(attributes, examples)

    #tree = decision_tree_learning(examples, attributes, parent_examples)

def decision_tree_learning(examples, attributes, parent_examples):
    if not examples:
        return plurality_value(parent_examples)
    elif all_example_classifications_are_equal(examples):
        return examples[0][-1] # return the classification
    elif not attributes:
        return plurality_value(examples)
    else:
        A = random_argmax(attributes, importance(a, examples))

def all_example_classifications_are_equal(examples):
    a = examples[0]
    for x in examples[1:]:
        if x != a:
            return False
    return True

def random_argmax(args):
    """
        Input: A sorted list
        Output: Random element of the elements on top tie
    """
    l = []
    for i in args[1:]:
        if i == args[0]: l.append(i)
        else: break
    return choice(l)

def random_argmax_dict(dict):
  """
    Input: A dictonary
    Output: A random selected element in the top tier
  """
  #returns the highest value in dict
  max_value = max(dict.values())
  # list all keys which match the highest value
  t = [key for key in dict.keys() if dict[key] == max_value]
  return choice(t)

def plurality_value(parent_examples):
    """
        Input: A list of elements
        Output: The most popular element in that list. Ties are returned randomly.
    """
    if not parent_examples: return None
    word_counter = {}
    for x in parent_examples:
        if x in word_counter:
            word_counter[x] += 1
        else:
            word_counter[x] = 1
    popular = sorted(word_counter, key = word_counter.get, reverse = True)
    return random_argmax(popular)

def importance(attributes, examples):
  if random:
    return choice(attributes)
  else:
    av = [attributes[key] for key,value in attributes.iteritems()]
    outcomes = [e[-1] for e in examples]
    avf = []
    for a in av:
      tmp = list(outcomes)
      for i in a:
        if i in tmp:
          tmp.remove(i)
      avf.append(tmp)
    
    # Calculate the information gain on each node
    b = {}
    for i in range(len(av)):
      b[i+1] = information_gain([av[i],avf[i]], outcomes)
    return random_argmax_dict(b)

    #return random_argmax(sorted([information_gain(examples, examples) for a in
    #  attributes]))
    
def information_gain(examples, parent_example):
  """
    Example Input:
        examples = [ [2,2],[1,1,1],[1,1,2,2,2,2] ]
        parent_example = [1,1,1,1,1,1,2,2,2,2,2,2]
    Output:
        0.54
  """
  N = float(len(parent_example))
  remainder = 0.0
  for a in examples:
    l = float(len(a))
    if l:
      r = B(a.count(1) / l)
      remainder += ((l / N) * r)
    #print "%s / %s * B(%s / %s)" % (l, N, a.count(1), l)
  #remainder = sum((float(len(a)) / N) * i for i in [B(a.count(1)/float(len(a)))
  #  for a in [e for e in examples]])
  
  #return B(p / len(examples)) - remainder
  #TODO: Calculate the B(p / p + n) instead of 1
  return 1 - remainder

def entropy(probabilities):
  return sum(-p * np.log2(p) for p in probabilities)

def B(q):
  if q == 0: return 0
  elif q == 1: return 0
  else: return -(q * np.log2(q) + ((1-q) * np.log2(1-q)))

def remove(list, val):
  return [value for value in list if value != val]

if __name__ == "__main__":
    main()
