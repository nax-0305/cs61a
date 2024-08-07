LAB_SOURCE_FILE=__file__


def double_eights(n):
    """ Returns whether or not n has two digits in row that
    are the number 8. Assume n has at least two digits in it.

    >>> double_eights(1288)
    True
    >>> double_eights(880)
    True
    >>> double_eights(538835)
    True
    >>> double_eights(284682)
    False
    >>> double_eights(588138)
    True
    >>> double_eights(78)
    False
    >>> from construct_check import check
    >>> # ban iteration
    >>> check(LAB_SOURCE_FILE, 'double_eights', ['While', 'For'])
    True
    """
    "*** YOUR CODE HERE ***"
    if n < 88:
        return False
    return n % 10 == 8 and n // 10 % 10 == 8 or double_eights(n // 10)


def make_onion(f, g):
    """Return a function can_reach(x, y, limit) that returns
    whether some call expression containing only f, g, and x with
    up to limit calls will give the result y.

    >>> up = lambda x: x + 1
    >>> double = lambda y: y * 2
    >>> can_reach = make_onion(up, double)
    >>> can_reach(5, 25, 4)      # 25 = up(double(double(up(5))))
    True
    >>> can_reach(5, 25, 3)      # Not possible
    False
    >>> can_reach(1, 1, 0)      # 1 = 1
    True
    >>> add_ing = lambda x: x + "ing"
    >>> add_end = lambda y: y + "end"
    >>> can_reach_string = make_onion(add_ing, add_end)
    >>> can_reach_string("cry", "crying", 1)      # "crying" = add_ing("cry")
    True
    >>> can_reach_string("un", "unending", 3)     # "unending" = add_ing(add_end("un"))
    True
    >>> can_reach_string("peach", "folding", 4)   # Not possible
    False
    """
    def can_reach(x, y, limit):
        if limit < 0:
            return False
        elif x == y:
            return True
        else:
            return can_reach(f(x), y, limit - 1) or can_reach(g(x), y, limit - 1)
    return can_reach


def mario_number(level):
    """Return the number of ways that Mario can perform a sequence of steps
    or jumps to reach the end of the level without ever landing in a Piranha
    plant. Assume that every level begins and ends with a space.

    >>> mario_number(' P P ')   # jump, jump
    1
    >>> mario_number(' P P  ')   # jump, jump, step
    1
    >>> mario_number('  P P ')  # step, jump, jump
    1
    >>> mario_number('   P P ') # step, step, jump, jump or jump, jump, jump
    2
    >>> mario_number(' P PP ')  # Mario cannot jump two plants
    0
    >>> mario_number('    ')    # step, jump ; jump, step ; step, step, step
    3
    >>> mario_number('    P    ')
    9
    >>> mario_number('   P    P P   P  P P    P     P ')
    180
    """
    "*** YOUR CODE HERE ***"
    # i, is_reach= 0, True
    # length, ways = len(level), 0
    # while i <= length - 3:
    #     if not is_reach:
    #         return 0
    #     if level[i:i+3] == '   ':
    #         ways = ways + 2
    #         i = i + 3
    #     elif level[i:i+3] == ' PP':
    #         is_reach = False
    #     elif level[i:i+3] == ' P ':
    #         ways = ways + 1
    #         i = i + 2
    #     elif level[i:i+3] == '  P':
    #         ways = ways + 1
    #         i = i + 1
    # return ways

    # 第一：是否是通路，如果不是通路就不可能
    # i, length = 0, len(level)
    # while i < length - 1:
    #     if level[i, i+2] == 'PP':
    #         return 0
    #     i = i + 1
    # # 在通路的情况下
    # def count_ways(level, i):

    if len(level) == 0:
        return 0
    if level == ' ':
        return 1
    elif level[-1] == 'P':
        return 0
    else:
        return mario_number(level[:len(level)-1]) + mario_number(level[:len(level)-2])



def max_subseq(n, t):
    """
    Return the maximum subsequence of length at most t that can be found in the given number n.
    For example, for n = 2012 and t = 2, we have that the subsequences are
        2
        0
        1
        2
        20
        21
        22
        01
        02
        12
    and of these, the maxumum number is 22, so our answer is 22.

    >>> max_subseq(2012, 2)
    22
    >>> max_subseq(20125, 3)
    225
    >>> max_subseq(20125, 5)
    20125
    >>> max_subseq(20125, 6) # note that 20125 == 020125
    20125
    >>> max_subseq(12345, 3)
    345
    >>> max_subseq(12345, 0) # 0 is of length 0
    0
    >>> max_subseq(12345, 1)
    5
    """
    "*** YOUR CODE HERE ***"

    # 完全偏离了正常的递归
    # 1. 剥离n不参与的后t-1位
    # 2. 在前digits(n) - t + 1位中找出最大的数的位d
    # 3. 将d的前几位去除，赋值给n，并将t减去1
    # 4. 重复1、2、3
    # 这个if-statement，虽然说解决了，但是不是学到的递归
    # def get_maxnumber(x):
    #     mn, i, c = 0, 0, x
    #     while c > 0:
    #         t = c % 10
    #         if mn < t:
    #             mn = t
    #         c = c // 10
    #     while x > 0:
    #         if x % 10 == mn:
    #             break
    #         i, x  = i + 1, x // 10
    #     return mn, i
    # mss = 0
    # while t > 0:
    #     tuple_maxnumber = get_maxnumber(n // pow(10, t-1))
    #     mss = mss + tuple_maxnumber[0] * pow(10, t-1)
    #     n = n % pow(10, tuple_maxnumber[1] + t - 1)
    #     t = t-1
    # return mss

    # 使用递归方法解决一下看看
    # 找到base case，当t为0

    # 这个递归是真的不会写！
    if t == 0:
        return 0
    elif n < 10:
        return n
    else:
        return max(max_subseq(n // 10, t-1) * 10 + n % 10, max_subseq(n // 10, t))


def is_prime(n):
    """
    >>> is_prime(7)
    True
    >>> is_prime(10)
    False
    >>> is_prime(1)
    False
    """
    "*** YOUR CODE HERE ***"
    if n == 1:
        return False
    def bigger_one_isprime(n, i):
        if i == 1:
            return True
        if n % i == 0:
            return False
        return bigger_one_isprime(n, i-1)
        

    return bigger_one_isprime(n, n-1)

