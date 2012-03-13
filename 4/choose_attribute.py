####
#  Herman Schistad
#  MTDT - NTNU - 2012
####

import numpy as np
from random import choice

random = True

class Node():
  spacing = ""
  def __init__(self, data):
    self.data = data
    self.children = {}

  def add_child(self, key, value):
    self.children[key] = value
  
  def print_node(self):
    print "%s" % self.data
    for key, value in self.children.iteritems():
      self.children[key].print_node()

class NodeLeaf():
  def __init__(self, data):
    self.data = data

  def print_node(self):
    print "L: %s" % self.data

def main():

    #### PARSING #####
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

    for i in range(len(examples)):
      for j in range(1,len(examples[i])):
        # For each attribute save the outcome if the attribute is true
        if examples[i][j] == "1":
          attributes[str(j)].append(examples[i][-1])

    
    # Lets ensure ourself that the information_gain function is working.
    # This should yield 0.54
    # examples = [ [2,2],[1,1,1],[1,1,2,2,2,2] ]
    # parent_example = [1,1,1,1,1,1,2,2,2,2,2,2]
    # print information_gain(examples, parent_example)
    
    parent_examples = None

    # Create the tree recursivly
    tree = decision_tree_learning(examples, attributes, parent_examples)
    return tree.print_node()

def decision_tree_learning(examples, attributes, parent_examples):
  """
    Example input:
      examples = [['1', '1', '2', '2', '1', '1', '1', '1'], ['1', '2', '2',
                  '1', '1', '1', '1', '1']]
      attributes = { 1: [1], 2: [1,2], ... }
      parent_examples = same as examples or None
    Output:
      A Node and NodeLeaf tree
  """
  if not examples:
      return NodeLeaf(plurality_value(parent_examples))
  elif all_example_classifications_are_equal(examples):
      return NodeLeaf(examples[0][-1]) # return the classification
  elif not attributes:
      return NodeLeaf(plurality_value(examples))
  else:
      A = int(importance(attributes, examples))
      
      # Create a root node based on A
      root = Node(A)
      
      exs = []
      for i in range(1,3):
        for row in range(len(examples)):
          if examples[row][A] == str(i):
            exs.append(examples[row])
        
        # Attributes - A
        at = removekey(attributes, str(A))

        subtree = decision_tree_learning(exs, at, examples)
        root.add_child(i, subtree)
      return root

def removekey(d, key):
  r = dict(d)
  del r[key]
  return r

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
    l = args[0]
    if len(args) > 1:
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
  print t
  return choice(t)

def plurality_value(parent_examples):
    """
        Input: A list of elements
        Output: The most popular element in that list. Ties are returned randomly.
    """
    if not parent_examples: return None
    word_counter = {}
    for x in parent_examples:
        if x[-1] in word_counter:
            word_counter[x[-1]] += 1
        else:
            word_counter[x[-1]] = 1
    popular = sorted(word_counter, key = word_counter.get, reverse = True)
    return random_argmax(popular)

def importance(attributes, examples):
  if random:
    return choice(attributes.keys())
  else:
    # av is just an array containing the values of each key
    av = [attributes[key] for key,value in attributes.iteritems()]
    outcomes = [e[-1] for e in examples]

    # Creates a "inverse" of the attribute values
    avf = []
    for a in av:
      tmp = list(outcomes)
      for i in a:
        if i in tmp:
          tmp.remove(i)
      avf.append(tmp)
     
    # Calculate the information gain on each node
    b = {}; i=0
    for key,value in attributes.iteritems():
      b[key] = information_gain([av[i],avf[i]], outcomes)
      i += 1
    return random_argmax_dict(b)

def information_gain(examples, parent_example):
  """
    Example Input:
        examples = [ [2,2],[1,1,1],[1,1,2,2,2,2] ]
        parent_example = [1,1,1,1,1,1,2,2,2,2,2,2]
    Output:
        0.54
  """
  #print examples
  #print parent_example
  N = float(len(parent_example))
  remainder = 0.0
  for a in examples:
    ones = a.count('1')
    l = float(len(a))
    if l:
      r = B(ones / l)
      remainder += ((l / N) * r)
      #print "%s / %s * B(%s / %s) - result: %s" % (l, N, ones, l, remainder)
    else: return 0
  return 1 - remainder

def entropy(probabilities):
  return sum(-p * np.log2(p) for p in probabilities)

def B(q):
  if q == 0 or q == 1: return 0
  else:
    return -(q * np.log2(q) + ((1-q) * np.log2(1-q)))

def remove(list, val):
  # Remove from list where not matching val
  return [value for value in list if value != val]

if __name__ == "__main__":
    main()
