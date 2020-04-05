from math import floor


def ordinal(n):
    """
    Return the ordinal string of a number
    """
    return "%d%s" % (n, "tsnrhtdd"[(floor(n/10) % 10 != 1)*(n % 10 < 4)*n % 10::4])
