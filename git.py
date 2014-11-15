import sh

class GitRepo(object):
    @staticmethod
    def factory(repopath):
        return sh.git.bake(_cwd=repopath)
