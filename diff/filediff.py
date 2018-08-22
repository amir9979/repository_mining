import difflib


class FileDiff(object):
    REMOVED = '- '
    ADDED = '+ '
    UNCHANGED = '  '
    NOT_IN_INPUT = '? '
    BEFORE_PREFIXES = [REMOVED, UNCHANGED]
    AFTER_PREFIXES = [ADDED, UNCHANGED]

    def __init__(self, diff):
        self.file_name = diff.b_path
        self.before_contents = diff.a_blob.data_stream[3].readlines()
        self.after_contents = diff.a_blob.data_stream[3].readlines()
        self.before_indices, self.after_indices = self.get_changed_indices()

    def get_changed_indices(self):
        def get_lines_by_prefixes(lines, prefixes):
            return  filter(lambda x: any(map(lambda p: x.startswith(p), prefixes)), lines)

        def get_indices_by_prefix(lines, prefix):
            return map(lambda x: x[0], filter(lambda x: x[1].startswith(prefix), enumerate(lines)))

        diff = list(difflib.ndiff(self.before_contents, self.after_contents))

        diff_before_lines = get_lines_by_prefixes(diff, self.BEFORE_PREFIXES)
        assert map(lambda x: x[2:], diff_before_lines) == self.before_contents
        before_indices = get_indices_by_prefix(diff_before_lines, self.REMOVED)

        diff_after_lines = get_lines_by_prefixes(diff, self.AFTER_PREFIXES)
        assert map(lambda x: x[2:], diff_after_lines) == self.after_contents
        after_indices = get_indices_by_prefix(diff_before_lines, self.ADDED)

        return before_indices, after_indices
