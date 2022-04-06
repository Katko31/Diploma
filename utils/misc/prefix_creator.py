import re


def get_prefix(sequence_name):
    prefix_search_pattern = '^[A-Z]+'
    if re.search(prefix_search_pattern, sequence_name) is not None:
        prefix = len((re.search(prefix_search_pattern, sequence_name)).group(0))
        return prefix
    else:
        return 5
