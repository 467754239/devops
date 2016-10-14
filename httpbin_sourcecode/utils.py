# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
httpbin.utils
~~~~~~~~~~~~~~~
Utility functions.
"""

import random
import bisect


def weighted_choice(choices):
    """Returns a value from choices chosen by weighted random selection
    choices should be a list of (value, weight) tuples.
    eg. weighted_choice([('val1', 5), ('val2', 0.3), ('val3', 1)])
    """

    # /status/418:2,403:3 ==> [(418, 2.0), (403, 3.0)]
    print choices

    values, weights = zip(*choices)
    total = 0
    cum_weights = []
    for w in weights:
        total += w
        cum_weights.append(total)
    print cum_weights

    x = random.uniform(0, total)        
    i = bisect.bisect(cum_weights, x)   # 以后看这个模块
    print "x>>>", x
    print values, i, values[i]
    return values[i]