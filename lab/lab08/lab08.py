def cumulative_mul(t):
    """Mutates t so that each node's label becomes the product of its own
    label and all labels in the corresponding subtree rooted at t.

    >>> t = Tree(1, [Tree(3, [Tree(5)]), Tree(7)])
    >>> cumulative_mul(t)
    >>> t
    Tree(105, [Tree(15, [Tree(5)]), Tree(7)])
    >>> otherTree = Tree(2, [Tree(1, [Tree(3), Tree(4), Tree(5)]), Tree(6, [Tree(7)])])
    >>> cumulative_mul(otherTree)
    >>> otherTree
    Tree(5040, [Tree(60, [Tree(3), Tree(4), Tree(5)]), Tree(42, [Tree(7)])])
    """
    "*** YOUR CODE HERE ***"
    # 这样的递归的方法已经实现了，但是就是返回值不对
    # if t.is_leaf():
    #     return t.label
    # for branch in t.branches:
    #     t.label = t.label * cumulative_mul(branch)
    # return t.label

    # 哈哈， 利用higher order function就解决了返回值的问题，芜湖
    def f(t):
        if t.is_leaf():
            return t.label
        for branch in t.branches:
            t.label = t.label * f(branch)
        return t.label
    f(t)

def delete(t, x):
    """Remove all nodes labeled x below the root within Tree t. When a non-leaf
    node is deleted, the deleted node's children become children of its parent.

    The root node will never be removed.

    >>> t = Tree(3, [Tree(2, [Tree(2), Tree(2)]), Tree(2), Tree(2, [Tree(2, [Tree(2), Tree(2)])])])
    >>> delete(t, 2)
    >>> t
    Tree(3)
    >>> t = Tree(1, [Tree(2, [Tree(4, [Tree(2)]), Tree(5)]), Tree(3, [Tree(6), Tree(2)]), Tree(4)])
    >>> delete(t, 2)
    >>> t
    Tree(1, [Tree(4), Tree(5), Tree(3, [Tree(6)]), Tree(4)])
    >>> t = Tree(1, [Tree(2, [Tree(4), Tree(5)]), Tree(3, [Tree(6), Tree(2)]), Tree(2, [Tree(6),  Tree(2), Tree(7), Tree(8)]), Tree(4)])
    >>> delete(t, 2)
    >>> t
    Tree(1, [Tree(4), Tree(5), Tree(3, [Tree(6)]), Tree(6), Tree(7), Tree(8), Tree(4)])
    """
    # new_branches = []
    # for b in t.branches:
    #     delete(b, x)
    #     if b.label == x:
    #         new_branches.append([])
    #     else:
    #         new_branches.append(b)
    # t.branches = new_branches

    # 终于写出来，这个
    new_branches = []
    for b in t.branches:
        # 要从上往下把label为x的删除，所以要从这个递归
        # 然后对当前的label判断，然后做动作
        delete(b, x)
        # 如果b.label == x，那么就把当前的 new_branch + b的branch
        # 如果b.label != x, 那么就把b添加到new_branches
        if b.label == x:
            new_branches = new_branches + b.branches
        else:
            new_branches.append(b)
    # 在本轮branch遍历结束后替换为new_branches，t.branches = new_branches
    t.branches = new_branches

def convert_link(link):
    """Takes a linked list and returns a Python list with the same elements.

    >>> link = Link(1, Link(2, Link(3, Link(4))))
    >>> convert_link(link)
    [1, 2, 3, 4]
    >>> convert_link(Link.empty)
    []
    """
    "*** YOUR CODE HERE ***"
    ret = []
    while link != Link.empty:
        ret.append(link.first)
        link = link.rest
    return ret

def add_links(link1, link2):
    """Adds two Links, returning a new Link

    >>> l1 = Link(1, Link(2))
    >>> l2 = Link(3, Link(4, Link(5)))
    >>> new = add_links(l1, l2)
    >>> print(new)
    <1 2 3 4 5>
    >>> new2 = add_links(l2,l1)
    >>> print(new2)
    <3 4 5 1 2>
    """
    "*** YOUR CODE HERE ***"
    # ret_link = Link.empty
    # while link1 != Link.empty:
    #     ret_link = Link(link1.first, ret_link)
    #     link1 = link1.rest
    # while link2 != Link.empty:
    #     ret_link = Link(link2.first, ret_link)
    #     link2 = link2.rest
    # return ret_link
    
    # 上面得程序结果是倒序得，看看利用递归，正序
    if link1.rest == Link.empty:
        return Link(link1.first)
    if link2.rest == Link.empty:
        return Link(link2.first)
    return Link(add_links(link1.rest, link2))
    add_links(link1, link2.rest)
    

def multiply_lnks(lst_of_lnks):
    """
    >>> a = Link(2, Link(3))
    >>> b = Link(5, Link(4))
    >>> p1 = multiply_lnks([a, b])
    >>> p1
    Link(10, Link(12))

    >>> c = Link(2, Link(3, Link(5)))
    >>> d = Link(6, Link(4, Link(2)))
    >>> e = Link(4, Link(1, Link(0, Link(2))))
    >>> p2 = multiply_lnks([c, d, e])
    >>> p2
    Link(48, Link(12, Link(0)))
    """
    product = 1
    for _________ in ________________:
        if __________________________________________:
            _________________________________
        ___________________
    lst_of_lnks_rests = [_________ for _________ in ________________]
    return _________________________________________________


class Tree:
    """
    >>> t = Tree(3, [Tree(2, [Tree(5)]), Tree(4)])
    >>> t.label
    3
    >>> t.branches[0].label
    2
    >>> t.branches[1].is_leaf()
    True
    """
    def __init__(self, label, branches=[]):
        for b in branches:
            assert isinstance(b, Tree)
        self.label = label
        self.branches = list(branches)

    def is_leaf(self):
        return not self.branches

    def __repr__(self):
        if self.branches:
            branch_str = ', ' + repr(self.branches)
        else:
            branch_str = ''
        return 'Tree({0}{1})'.format(self.label, branch_str)

    def __str__(self):
        def print_tree(t, indent=0):
            tree_str = '  ' * indent + str(t.label) + "\n"
            for b in t.branches:
                tree_str += print_tree(b, indent + 1)
            return tree_str
        return print_tree(self).rstrip()


class Link:
    """A linked list.

    >>> s = Link(1)
    >>> s.first
    1
    >>> s.rest is Link.empty
    True
    >>> s = Link(2, Link(3, Link(4)))
    >>> s.first = 5
    >>> s.rest.first = 6
    >>> s.rest.rest = Link.empty
    >>> s                                    # Displays the contents of repr(s)
    Link(5, Link(6))
    >>> s.rest = Link(7, Link(Link(8, Link(9))))
    >>> s
    Link(5, Link(7, Link(Link(8, Link(9)))))
    >>> print(s)                             # Prints str(s)
    <5 7 <8 9>>
    """
    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is not Link.empty:
            rest_repr = ', ' + repr(self.rest)
        else:
            rest_repr = ''
        return 'Link(' + repr(self.first) + rest_repr + ')'

    def __str__(self):
        string = '<'
        while self.rest is not Link.empty:
            string += str(self.first) + ' '
            self = self.rest
        return string + str(self.first) + '>'

