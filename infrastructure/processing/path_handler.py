class PathHandler:
    @staticmethod
    def path_basename(path) -> str:
        import os
        return os.path.splitext(os.path.basename(path))[0]