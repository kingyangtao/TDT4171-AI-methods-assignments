mport numpy

def main():
    examples = None
    attributes = None
    parent_examples = None
    tree = decision_tree_learning(examples, attributes, parent_examples)

def decision_tree_learning(examples, attributes, parent_examples):
    if not examples:
        return plurality_value(parent_examples)
    else if all_example_classifications_are_equal(examples):
        return examples[0][-1] # return the classification
    else if not attributes:
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

def plurality_value(parent_examples):
    """
        Input: A list of elements
        Output: The most popular element in that list. Ties are returned randomly.
    """
    if not parent_examples return None
    word_counter = {}
    for x in parent_examples:
        if x in word_counter:
            word_counter[x] += 1
        else:
            word_counter[x] = 1
    popular = sorted(word_counter, key = word_counter.get, reverse = True)
    return random_argmax(popular)

def importance(attributes, examples):
    def I(examples):
        return information_content([count(target, v, examples) for v in values

if __name__ == "__main__":
    main()
