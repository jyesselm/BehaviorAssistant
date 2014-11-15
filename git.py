import sh

class GitRepo(object):
    @staticmethod
    def factory(self, repopath):
        return sh.git.bake(_cwd=repopath)
