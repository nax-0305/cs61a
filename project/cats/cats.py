"""Typing test implementation"""

from utils import (
    lower,
    split,
    # 去除标点符号
    remove_punctuation,
    lines_from_file,
    count,
    deep_convert_to_tuple,
)
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


# 在一段话（paragraphs）中，选择第k个满足select函数的string or word
def pick(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which the SELECT returns True.
    If there are fewer than K such paragraphs, return an empty string.

    Arguments:
        paragraphs: a list of strings representing paragraphs
        select: a function that returns True for paragraphs that meet its criteria
        k: an integer

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> pick(ps, s, 0)
    'hi'
    >>> pick(ps, s, 1)
    'fine'
    >>> pick(ps, s, 2)
    ''
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    # i, kth = 0, 0
    # while i < len(paragraphs):
    #     cur = paragraphs[i]
    #     if select(cur):
    #         if kth == k:
    #             return cur
    #         else:
    #             kth = kth + 1
    #     i = i + 1
    # return ''

    # yes！！ recursion version done
    if len(paragraphs) == 0:
        return ''
    if select(paragraphs[0]):
        if k == 0:
            return paragraphs[0]
        else:
            return pick(paragraphs[1:], select, k-1)
    return pick(paragraphs[1:], select, k)
    
    # END PROBLEM 1


# about接受一个string list， 返回一个函数exist_in(paragraph)。
# exist_in接受一个paragraph，返回string_list中的strings是否有存在于paragraph
def about(subject):
    """Return a function that takes in a paragraph and returns whether
    that paragraph contains one of the words in SUBJECT.

    Arguments:
        subject: a list of words related to a subject

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in subject]), "subjects should be lowercase."

    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def exist_in(paragraph):
        str_list = split(paragraph)
        for str in str_list:
            for item in subject:
                if lower(remove_punctuation(str)) == item:
                    return True
        return False
    return exist_in
    # END PROBLEM 2


# 在参数typed和source两个字符串中，逐个判断每个word（根据空格划分）是否相等
# 计算规则如下，计算typed的正确率
def accuracy(typed, source):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    compared to the corresponding words in SOURCE.

    Arguments:
        typed: a string that may contain typos
        source: a model string without errors

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0
    """
    typed_words = split(typed)
    source_words = split(source)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    # 1. 两个list的长度都是0，则100.0
    # 2. 两个list的长度只有一个为0，则0.0   (这个check必为0，也是check / tlen)
    # 3. 两个list的长度都不为0，则 check / tlen
    tlen, slen = len(typed_words), len(source_words)
    if tlen == 0 and slen == 0:
        return 100.0
    i, check = 0, 0
    while i < tlen:
        if slen == i:
            break
        if typed_words[i] == source_words[i]:
            check = check + 1
        i = i + 1
    return (check / tlen) * 100.0 if check != 0 else 0.0
    # END PROBLEM 3


# 计算words per minute，这个words是根据typed字符串的长度除以5，而不是真正的word个数
def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string.

    Arguments:
        typed: an entered string
        elapsed: an amount of time in seconds

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0
    """
    assert elapsed > 0, "Elapsed time must be positive"
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    return (len(typed) / 5) / (elapsed / 60)
    # END PROBLEM 4


################
# Phase 4 (EC) #
################


def memo(f):
    """A general memoization decorator."""
    cache = {}

    def memoized(*args):
        immutable_args = deep_convert_to_tuple(args)  # convert *args into a tuple representation
        if immutable_args not in cache:
            result = f(*immutable_args)
            cache[immutable_args] = result
            return result
        return cache[immutable_args]

    return memoized


# 第7个问题，我的base case可以通过用例，但是没法使用这个装饰器
def memo_diff(diff_function):
    """A memoization function."""
    cache = {}

    def memoized(typed, source, limit):
        # BEGIN PROBLEM EC
        if (typed, source) in cache and limit <= cache[(typed, source)][1]:
            return cache[(typed, source)][0]
        else:
            value = diff_function(typed, source, limit)
            cache[(typed, source)] = [value, limit]
            return value
        # END PROBLEM EC
    return memoized


###########
# Phase 2 #
###########


# 从已有的word_list中找出最接近typed_word的word代替
# 如何找到？
# 使用diff_function，由这个函数决定
@memo
def autocorrect(typed_word, word_list, diff_function, limit):
    """Returns the element of WORD_LIST that has the smallest difference
    from TYPED_WORD based on DIFF_FUNCTION. If multiple words are tied for the smallest difference,
    return the one that appears closest to the front of WORD_LIST. If the
    difference is greater than LIMIT, return TYPED_WORD instead.

    Arguments:
        typed_word: a string representing a word that may contain typos
        word_list: a list of strings representing source words
        diff_function: a function quantifying the difference between two words
        limit: a number

    >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    # 1. 如果typed_word在word_list中，那么返回typed_word
    # 2. 如果不在，则根据diff_function，将typed_word与word_list中的word一一比较不同，返回difference最小的word
    # 3. 如果任何一个difference都超过limit，则返回typed_word
    # 4. 如果有多个最小difference，那么返回word_list中靠前的word
    diff_word_list, diff_list = [], []
    for word in word_list:
        if word == typed_word:
            return word
        word_diff = diff_function(typed_word, word, limit)
        diff_list.append(word_diff)
        diff_word_list.append((word_diff, word))
    # print(diff_word_list)
    min_diff = min(diff_list, key=abs)
    last_word = [diff_word[1] for diff_word in diff_word_list if diff_word[0] <= limit and diff_word[0] == min_diff]
    # print(last_word)
    return typed_word if len(last_word) == 0 else last_word[0]
    # END PROBLEM 5


# 这个diff_function，比autocorrect中举例的函数要高级一点，是根据两个字符串对应字符的是否相同来决定的
def furry_fixes(typed, source, limit):
    """A diff function for autocorrect that determines how many letters
    in TYPED need to be substituted to create SOURCE, then adds the difference in
    their lengths and returns the result.

    Arguments:
        typed: a starting word
        source: a string representing a desired goal word
        limit: a number representing an upper bound on the number of chars that must change

    >>> big_limit = 10
    >>> furry_fixes("nice", "rice", big_limit)    # Substitute: n -> r
    1
    >>> furry_fixes("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
    2
    >>> furry_fixes("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
    3
    >>> furry_fixes("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
    5
    >>> furry_fixes("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
    5
    """
    # BEGIN PROBLEM 6
    # 使用递归，
    if limit < 0:
        return 1
    t_len, s_len = len(typed), len(source)
    if t_len == 0 or s_len == 0:
        return t_len + s_len
    is_differ_char = 1
    if typed[0] == source[0]:
        is_differ_char = 0
    else:
        limit = limit - 1
    return is_differ_char + furry_fixes(typed[1:], source[1:], limit)
    # END PROBLEM 6


# 这又是一个differ_function，
@memo_diff
def minimum_mewtations(typed, source, limit):
    """A diff function for autocorrect that computes the edit distance from TYPED to SOURCE.
    This function takes in a string TYPED, a string SOURCE, and a number LIMIT.

    Arguments:
        typed: a starting word
        source: a string representing a desired goal word
        limit: a number representing an upper bound on the number of edits

    >>> big_limit = 10
    >>> minimum_mewtations("cats", "scat", big_limit)       # cats -> scats -> scat
    2
    >>> minimum_mewtations("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> minimum_mewtations("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3
    """
    # Base cases should go here, you may add more base cases as needed.
    if limit < 0:
        return 1
    if typed == source:
        return 0
    # 为什么要有这个基础条件，是因为在remove之后，可能会出现空字符串的情况，所以要这么处理
    t_len, s_len = len(typed), len(source)
    if t_len == 0 or s_len == 0:
        return t_len + s_len
    # 递归，首字母是否相同
    if typed[0] == source[0]:
        return minimum_mewtations(typed[1:], source[1:], limit)
    else:
        # 这里如果能用lambda表达式的话，那么将很符合题意
        # add = lambda list_typed, c: ''.join(list_typed.insert(0, c))
        # remove = lambda list_typed: ''.join(list_typed.remove(list_typed[0]))
        # substitute = lambda list_typed, c: add(list(remove(list_typed), c))
        addcase_list, rmcase_list, substitutecase_list = list(typed), list(typed), list(typed)
        addcase_list.insert(0, source[0])
        rmcase_list.remove(rmcase_list[0])
        substitutecase_list[0] = source[0]
        # 这块的思路是对的，在当前情况下找到最小的
        return 1 + min([minimum_mewtations(''.join(addcase_list), source, limit - 1), 
                        minimum_mewtations(''.join(rmcase_list), source, limit - 1), 
                        minimum_mewtations(''.join(substitutecase_list), source, limit - 1)])

    # solution from cs61a 
    # if typed == "" or source == "":
    #     return max(len(typed), len(source))
    # elif limit == 0:
    #     return int(typed!=source)
    # elif typed == source:
    #     return 0
    # elif typed[0] == source[0]:
    #     return minimum_mewtations(typed[1:], source[1:], limit)
    # else:
    #     # 这里是用的逆向思维，增加、删除、替换的操作
    #     add = 1 + minimum_mewtations(typed, source[1:], limit-1)
    #     remove = 1 + minimum_mewtations(typed[1:], source, limit-1)
    #     substitute = 1 + minimum_mewtations(typed[1:], source[1:], limit-1)
    # return min(add, min(remove, substitute))

# Ignore the line below
minimum_mewtations = count(minimum_mewtations)


def final_diff(typed, source, limit):
    """A diff function that takes in a string TYPED, a string SOURCE, and a number LIMIT.
    If you implement this function, it will be used."""
    assert False, "Remove this line to use your final_diff function."


FINAL_DIFF_LIMIT = 6  # REPLACE THIS WITH YOUR LIMIT


###########
# Phase 3 #
###########


def report_progress(typed, source, user_id, upload):
    """Upload a report of your id and progress so far to the multiplayer server.
    Returns the progress so far.

    Arguments:
        typed: a list of the words typed so far
        source: a list of the words in the typing source
        user_id: a number representing the id of the current user
        upload: a function used to upload progress to the multiplayer server

    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> # The above function displays progress in the format ID: __, Progress: __
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> typed = ['how', 'are', 'you']
    >>> source = ['how', 'are', 'you', 'doing', 'today']
    >>> report_progress(typed, source, 2, print_progress)
    ID: 2 Progress: 0.6
    0.6
    >>> report_progress(['how', 'aree'], source, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    # BEGIN PROBLEM 8
    i, progress = 0, 0
    correct, t_len = 0, len(typed)
    while i < t_len:
        if typed[i] != source[i]:
            break
        correct, i = correct + 1, i + 1
    progress = correct / len(source)
    id_progress = {'id': user_id, 'progress': progress}
    upload(id_progress)
    return progress
    # END PROBLEM 8


def time_per_word(words, timestamps_per_player):
    """Return two values: the list of words that the players are typing and
    a list of lists that stores the durations it took each player to type each word.

    Arguments:
        words: a list of words, in the order they are typed.
        TIMESTAMPS_PER_PLAYER: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.


    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> words, times = time_per_word(['collar', 'plush', 'blush', 'repute'], p)
    >>> words
    ['collar', 'plush', 'blush', 'repute']
    >>> times
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    # BEGIN PROBLEM 9
    times = []
    for t_list in timestamps_per_player:
        i, t_list_len = 0, len(t_list)
        tmp_list = []
        while i < t_list_len - 1:
            tmp_list.append(t_list[i+1] - t_list[i])
            i = i + 1
        times.append(tmp_list)
    return words, times
    # END PROBLEM 9


def time_per_word_match(words, timestamps_per_player):
    """Return a match object containing the words typed and the time it took each player to type each word.

    Arguments:
        words: a list of words, in the order they are typed.
        timestamps_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.

    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> match_object = time_per_word_match(['collar', 'plush', 'blush', 'repute'], p)
    >>> get_all_words(match_object)    # Notice how we now use the selector functions to access the data
    ['collar', 'plush', 'blush', 'repute']
    >>> get_all_times(match_object)
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    # BEGIN PROBLEM 11
    words, times = time_per_word(words, timestamps_per_player)
    return match(words, times)
    # END PROBLEM 11


def fastest_words(match_object):
    """Return a list of lists indicating which words each player typed the fastest.

    Arguments:
        match_object: a match data abstraction created by the match constructor

    >>> p0 = [5, 1, 3]
    >>> p1 = [4, 1, 6]
    >>> fastest_words(match(['Just', 'have', 'fun'], [p0, p1]))
    [['have', 'fun'], ['Just']]
    >>> p0  # input lists should not be mutated
    [5, 1, 3]
    >>> p1
    [4, 1, 6]
    """
    player_indices = range(len(get_all_times(match_object)))  # contains an *index* for each player
    word_indices = range(len(get_all_words(match_object)))  # contains an *index* for each word
    # BEGIN PROBLEM 11
    i, j =0, 0
    fast_list = [[] for i in player_indices]
    for i in word_indices:
        min_pnumber, min_time = 0, get_time(match_object, 0, i)
        for j in player_indices:
            j_time = get_time(match_object, j, i)
            if j_time < min_time:
                min_pnumber, min_time = j, j_time

        fast_list[min_pnumber].append(get_word(match_object, i))
    return fast_list
    # END PROBLEM 11


def match(words, times):
    """Creates a data abstraction containing all words typed and their times.

    Arguments:
        words: A list of strings, each string representing a word typed.
        times: A list of lists for how long it took for each player to type
            each word.
            times[i][j] = time it took for player i to type words[j].

    Example input:
        words: ['Hello', 'world']
        times: [[5, 1], [4, 2]]
    """
    assert all([type(w) == str for w in words]), "words should be a list of strings"
    assert all([type(t) == list for t in times]), "times should be a list of lists"
    assert all([isinstance(i, (int, float)) for t in times for i in t]), "times lists should contain numbers"
    assert all([len(t) == len(words) for t in times]), "There should be one word per time."
    return {"words": words, "times": times}


def get_word(match, word_index):
    """A utility function that gets the word with index word_index"""
    assert (0 <= word_index < len(get_all_words(match))), "word_index out of range of words"
    return get_all_words(match)[word_index]


def get_time(match, player_num, word_index):
    """A utility function for the time it took player_num to type the word at word_index"""
    assert word_index < len(get_all_words(match)), "word_index out of range of words"
    assert player_num < len(get_all_times(match)), "player_num out of range of players"
    return get_all_times(match)[player_num][word_index]


def get_all_words(match):
    """A selector function for all the words in the match"""
    return match["words"]


def get_all_times(match):
    """A selector function for all typing times for all players"""
    return match["times"]


def match_string(match):
    """A helper function that takes in a match data abstraction and returns a string representation of it"""
    return f"match({get_all_words(match)}, {get_all_times(match)})"


enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file("data/sample_paragraphs.txt")
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        source = pick(paragraphs, select, i)
        if not source:
            print("No more paragraphs about", topics, "are available.")
            return
        print("Type the following paragraph and then press enter/return.")
        print("If you only type part of it, you will be scored only on that part.\n")
        print(source)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print("Goodbye.")
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print("Words per minute:", wpm(typed, elapsed))
        print("Accuracy:        ", accuracy(typed, source))

        print("\nPress enter/return for the next paragraph or type q to quit.")
        if input().strip() == "q":
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse

    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument("topic", help="Topic word", nargs="*")
    parser.add_argument("-t", help="Run typing test", action="store_true")

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)