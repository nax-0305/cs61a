def hailstone(n):
    """Q1: Yields the elements of the hailstone sequence starting at n.
       At the end of the sequence, yield 1 infinitely.

    >>> hail_gen = hailstone(10)
    >>> [next(hail_gen) for _ in range(10)]
    [10, 5, 16, 8, 4, 2, 1, 1, 1, 1]
    >>> next(hail_gen)
    1
    """
    "*** YOUR CODE HERE ***"
    # yield key word
    while n > 0:
        yield n
        if n % 2 == 0:
            n = n // 2
        elif n > 1 and n % 2 == 1:
            n = 3 * n + 1

def merge(a, b):
    """Q2:
    >>> def sequence(start, step):
    ...     while True:
    ...         yield start
    ...         start += step
    >>> a = sequence(2, 3) # 2, 5, 8, 11, 14, ...
    >>> b = sequence(3, 2) # 3, 5, 7, 9, 11, 13, 15, ...
    >>> result = merge(a, b) # 2, 3, 5, 7, 8, 9, 11, 13, 14, 15
    >>> [next(result) for _ in range(10)]
    [2, 3, 5, 7, 8, 9, 11, 13, 14, 15]
    """
    "*** YOUR CODE HERE ***"
    cur_a, cur_b = next(a), next(b)
    while True:
        ret = 0
        if cur_a < cur_b:
            ret = cur_a
            cur_a = next(a) 
        elif cur_a == cur_b:
            ret = cur_a
            cur_a = next(a)
            cur_b = next(b)
        else:
            ret = cur_b
            cur_b = next(b)
        yield ret

    # solution from cs61a
    # first_a, first_b = next(a), next(b)
    # while True:
    #     if first_a == first_b:
    #         yield first_a
    #         first_a, first_b = next(a), next(b)
    #     elif first_a < first_b:
    #         yield first_a
    #         first_a = next(a)
    #     else:
    #         yield first_b
    #         first_b = next(b)

def perms(seq):
    """Q3: Generates all permutations of the given sequence. Each permutation is a
    list of the elements in SEQ in a different order. The permutations may be
    yielded in any order.

    >>> p = perms([100])
    >>> type(p)
    <class 'generator'>
    >>> next(p)
    [100]
    >>> try: # Prints "No more permutations!" if calling next would cause an error
    ...     next(p)
    ... except StopIteration:
    ...     print('No more permutations!')
    No more permutations!
    >>> sorted(perms([1, 2, 3])) # Returns a sorted list containing elements of the generator
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    >>> sorted(perms((10, 20, 30)))
    [[10, 20, 30], [10, 30, 20], [20, 10, 30], [20, 30, 10], [30, 10, 20], [30, 20, 10]]
    >>> sorted(perms("ab"))
    [['a', 'b'], ['b', 'a']]
    """
    "*** YOUR CODE HERE ***"
    # s, n = list(seq), len(seq)
    # if n == 1:
    #     yield s 
    # for p in perms(s[:n-1]):
    #     for i in range(len(p) + 1):
    #         temp = p.copy()
    #         temp.insert(i, s[-1])
    #         i = i + 1
    #         yield temp

    # solution from cs61a
    if not seq:
        yield []
    else:
        for p in perms(seq[1:]):
            for i in range(len(seq)):
                yield p[:i] + [seq[0]] + p[i:]



def yield_paths(t, value):
    """Q4: Yields all possible paths from the root of t to a node with the label
    value as a list.

    >>> t1 = tree(1, [tree(2, [tree(3), tree(4, [tree(6)]), tree(5)]), tree(5)])
    >>> print_tree(t1)
    1
      2
        3
        4
          6
        5
      5
    >>> next(yield_paths(t1, 6))
    [1, 2, 4, 6]
    >>> path_to_5 = yield_paths(t1, 5)
    >>> sorted(list(path_to_5))
    [[1, 2, 5], [1, 5]]

    >>> t2 = tree(0, [tree(2, [t1])])
    >>> print_tree(t2)
    0
      2
        1
          2
            3
            4
              6
            5
          5
    >>> path_to_2 = yield_paths(t2, 2)
    >>> sorted(list(path_to_2))
    [[0, 2], [0, 2, 1, 2]]
    """
    if label(t) == value:
        yield [value]
    for b in branches(t):
        for y in yield_paths(b, value):
            yield [label(t)] + y
    

class Minty:
    """A mint creates coins by stamping on years. The update method sets the mint's stamp to Minty.present_year.
    >>> mint = Minty()
    >>> mint.year
    2021
    >>> dime = mint.create('Dime')
    >>> dime.year
    2021
    >>> Minty.present_year = 2101  # Time passes
    >>> nickel = mint.create('Nickel')
    >>> nickel.year     # The mint has not updated its stamp yet
    2021
    >>> nickel.worth()  # 5 cents + (80 - 50 years)
    35
    >>> mint.update()   # The mint's year is updated to 2101
    >>> Minty.present_year = 2176     # More time passes
    >>> mint.create('Dime').worth()    # 10 cents + (75 - 50 years)
    35
    >>> Minty().create('Dime').worth()  # A new mint has the current year
    10
    >>> dime.worth()     # 10 cents + (155 - 50 years)
    115
    """
    present_year = 2021

    def __init__(self):
        self.update()

    def create(self, type):
        "*** YOUR CODE HERE ***"
        return Coin(self.year, type)

    def update(self):
        "*** YOUR CODE HERE ***"
        self.year = Minty.present_year

class Coin:
    cents = 50

    def __init__(self, year, type):
        "*** YOUR CODE HERE ***"
        self.year = year
        self.type = type

    def worth(self):
        "*** YOUR CODE HERE ***"
        value = 0
        if self.type == 'Nickel':
            value = 5
        elif self.type == 'Dime':
            value = 10
        over = Minty.present_year - self.year - self.cents
        return value if over < 0 else value + over
    
    # solution from cs61a
    # def __init__(self, year, type):
    #     self.year = year
    #     if type == ('Dime'):
    #         self.cents = 10
    #     elif type == ('Nickel'):
    #         self.cents = 5

    # def worth(self):
    #     return self.cents + max(0, Minty.present_year - self.year - 50)

class VendingMachine:
    """A vending machine that vends some product for some price.

    >>> v = VendingMachine('candy', 10)
    >>> v.vend()
    'Nothing left to vend. Please restock.'
    >>> v.add_funds(15)
    'Nothing left to vend. Please restock. Here is your $15.'
    >>> v.restock(2)
    'Current candy stock: 2'
    >>> v.vend()
    'Please add $10 more funds.'
    >>> v.add_funds(7)
    'Current balance: $7'
    >>> v.vend()
    'Please add $3 more funds.'
    >>> v.add_funds(5)
    'Current balance: $12'
    >>> v.vend()
    'Here is your candy and $2 change.'
    >>> v.add_funds(10)
    'Current balance: $10'
    >>> v.vend()
    'Here is your candy.'
    >>> v.add_funds(15)
    'Nothing left to vend. Please restock. Here is your $15.'

    >>> w = VendingMachine('soda', 2)
    >>> w.restock(3)
    'Current soda stock: 3'
    >>> w.restock(3)
    'Current soda stock: 6'
    >>> w.add_funds(2)
    'Current balance: $2'
    >>> w.vend()
    'Here is your soda.'
    """
    "*** YOUR CODE HERE ***"
    def __init__(self, product, price):
        self.product = product
        self.price = price
        self.remaining = 0
        self.cur_balance = 0

    def vend(self):
        if self.remaining == 0:
            return f'Nothing left to vend. Please restock.'
        else:
            if self.cur_balance < self.price:
                return f'Please add ${self.price - self.cur_balance} more funds.'
            elif self.cur_balance == self.price:
                self.remaining = self.remaining - 1
                self.cur_balance = 0
                return f'Here is your {self.product}.'
            else:
                self.remaining = self.remaining - 1
                change = self.cur_balance - self.price
                self.cur_balance = 0
                return f'Here is your {self.product} and ${change} change.'

    def add_funds(self, cash):
        if self.remaining <= 0:
            return f'Nothing left to vend. Please restock. Here is your ${cash}.'
        else:
            self.cur_balance = self.cur_balance + cash
            return f'Current balance: ${self.cur_balance}'

    def restock(self, num):
        self.remaining = self.remaining + num
        return f'Current {self.product} stock: {self.remaining}'

    
# Tree Data Abstraction

def tree(label, branches=[]):
    """Construct a tree with the given label value and a list of branches."""
    for branch in branches:
        assert is_tree(branch), 'branches must be trees'
    return [label] + list(branches)

def label(tree):
    """Return the label value of a tree."""
    return tree[0]

def branches(tree):
    """Return the list of branches of the given tree."""
    return tree[1:]

def is_tree(tree):
    """Returns True if the given tree is a tree, and False otherwise."""
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True

def is_leaf(tree):
    """Returns True if the given tree's list of branches is empty, and False
    otherwise.
    """
    return not branches(tree)

def print_tree(t, indent=0):
    """Print a representation of this tree in which each node is
    indented by two spaces times its depth from the root.

    >>> print_tree(tree(1))
    1
    >>> print_tree(tree(1, [tree(2)]))
    1
      2
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> print_tree(numbers)
    1
      2
      3
        4
        5
      6
        7
    """
    print('  ' * indent + str(label(t)))
    for b in branches(t):
        print_tree(b, indent + 1)

def copy_tree(t):
    """Returns a copy of t. Only for testing purposes.

    >>> t = tree(5)
    >>> copy = copy_tree(t)
    >>> t = tree(6)
    >>> print_tree(copy)
    5
    """
    return tree(label(t), [copy_tree(b) for b in branches(t)])

