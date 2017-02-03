from __future__ import division, print_function, absolute_import
import sys
import numpy as np

def split_iter(lst, token):
    """Split a list on the token, yield head and tail."""
    idx  = lst.index(token)
    return lst[:idx], lst[idx+1:]


def split_list(lst, token=' -----\n'):
    res = []
    head = lst
    try:
        while True:
            head, tail = split_iter(head, token)
            res.append(head)
            head = tail
    except ValueError:
        # we're done, it seems
        pass
    return res

## test case, trivial
#lst = [1, 2, 3, -1, 4, 5, -1, 6, 7, -1, 8]
#print(split_list(lst, token=-1))

def convert_replica(lst):
    """Parse the lines for a single replica."""
    assert len(lst) == 6
    lst_s = [elem.split('!') for elem in lst]

    r = {}
    for pair in lst_s:
        assert len(pair) == 2
        names = pair[1].strip().split(',')
        values = [float(_) for _ in pair[0].split()]
        for name, val in zip(names, values):
            r[name.strip()] = val

    return r



if __name__ == "__main__":
    fname = sys.argv[1]

    with open(fname) as f:
        lines = f.readlines()

    # XXX: skip header for now
    str_replicas = split_list(lines)
    str_replicas = str_replicas[1:]

    # convert: replicas will be a list of dicts of {name: value}
    replicas = [convert_replica(str_replica) for str_replica in str_replicas]

    # compute the Binder cumulant
    m2 = np.asarray([_["av_m2"] for _ in replicas])
    err_m2 = np.asarray([_["err_m2"] for _ in replicas])

    m4 = np.asarray([_["av_m4"] for _ in replicas])
    err_m4 = np.asarray([_["err_m4"] for _ in replicas])

    Q = 1. - m4/3.0/m2**2
    err_Q = (2*err_m2 / m2)**2 + (err_m4 / m4)
    err_Q = np.sqrt(err_Q) * Q

    print(Q)
    print(err_Q)

    print("num replicas = ", Q.size)
    print("Binder Q = ", Q.mean(), Q.std())

    import matplotlib.pyplot as plt
    plt.hist(Q)
    plt.show()
