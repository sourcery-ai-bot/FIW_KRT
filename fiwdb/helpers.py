import fiwdb.database as db
import warnings as warn
import numpy as np


def check_npairs(npairs, ktype, fid):
    """
    Check tht pair counter is greater than 0 and even (i.e., for each element there is a corresponding pair.
    :param npairs:
    :return:    True if both test passes
    """
    if npairs == 0:
        print("No " + ktype + " in " + str(fid))
        return False
    if npairs % 2 != 0:
        warn.warn("Number of pairs should be even, but there are" + str(npairs))
        return False

    return True


def compare_mid_lists(list1, list2):
    """
    Compares sizes and contents of 2 lists.
    :param list1:
    :param list2:
    :return: True, True: if both sizes and contents are equal; True, False: size same, content differs; etc.
    """

    same_size = True
    same_contents = True

    if len(list1) != len(list2):
        same_size = False

    if list1 != list2:
        same_contents = False

    return same_size, same_contents


def check_rel_matrix(rel_matrix, fid=''):
    """

    :param rel_matrix:
    :return:    True if matrix passes all tests
    """
    passes = True
    messages = []
    # check diagonal is all zeros
    if any(rel_matrix.diagonal() != 0):
        messages.append("Non-zero elements found in diagonal of relationship matrix ({})".format(fid))
        warn.warn(messages[len(messages) - 1])
        passes = False

    rids = db.load_rid_lut()

    pair_types = [(rids.RID[1], rids.RID[1]),  # siblings
                  (rids.RID[0], rids.RID[3]),  # parent-child
                  (rids.RID[2], rids.RID[5]),  # grandparent-grandchild
                  (rids.RID[4], rids.RID[4]),  # spouses
                  (rids.RID[6], rids.RID[7])  # great-grandparent-great-grandchild
                  ]

    # check that matrix elements of upper/ lower triangle correspond (e.g., 4 at (4,3) means 1 at (3, 4)
    # do this for each type
    for int_pair in pair_types:
        n_mismatches = (np.where(rel_matrix == int_pair[0], 1, 0) - np.where(rel_matrix == int_pair[1], 1, 0).T).sum()

        if n_mismatches > 0:
            messages.append("Inconsistent labels ({}) in relationship matrix ({}) for RIDs {}".format(n_mismatches,
                                                                                                      fid,
                                                                                                      int_pair))
            warn.warn(messages[len(messages) - 1])
            passes = False

    return passes, messages
