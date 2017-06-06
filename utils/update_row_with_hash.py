import hashlib
import operator


def update_with_hash(single_dictionary):

    sorted_x = sorted(single_dictionary.items(), key=operator.itemgetter(0))

    hash_ = hashlib.md5()
    hash_.update(str(sorted_x))
    single_dictionary.update({'Hash': hash_.hexdigest()})

    return single_dictionary