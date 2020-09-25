
class StringUtils(object):

    @staticmethod
    def truncateString(full_string, delimiter, max_string_length):
        slices = full_string.split(delimiter)
        accumulator = []
        count = 0
        for s in slices:
            if ((len(s) + count) <= max_string_length):
                accumulator.append(s)
                count += len(s) + len(delimiter)
            else:
                break

        result = delimiter.join(accumulator)
        return result
