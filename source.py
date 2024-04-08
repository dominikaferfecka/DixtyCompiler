import io


class Source:
    def __init__(self):
        self._source = None

    def read(self):
        return self._source.read(1)


class SourceFile(Source):
    def __init__(self, file_path):
        super().__init__()
        self._source = open(file_path, 'r')


class SourceString(Source):
    def __init__(self, string):
        super().__init__()
        self._source = io.StringIO(string)
