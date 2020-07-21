class CSV:
    def __init__(self, fileName):
        self.file = open(fileName, 'a')

    def append(self, dat):
        self.file.write(dat)

    def close(self):
        self.file.flush()
        self.file.close()




