import io


class Source:
    def __init__(self):
        self._source = None

class SourceFile(Source):
    def __init__(self, file_path):
        super().__init__()
        self._file_path = file_path
    
    def __enter__(self):
        self._source = open(self._file_path, 'r')
        return self._source

    def __exit__(self, exc_type, exc_value, traceback):
        self._source.close()


class SourceString(Source):
    def __init__(self, string):
        super().__init__()
        self._source = io.StringIO(string)
    
    def read(self, number):
        return self._source.read(number)

    
