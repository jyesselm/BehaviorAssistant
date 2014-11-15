from BehaviorAssistant.git import GitRepo

class LogEntry(object):
    def __init__(self, name, time):
        self.name = name
        self.time = time


class Log(object):

    def __init__(self, repopath, branch, template=None):
        self.repo = GitRepo.factory(repopath)
        self.template = template
        self.branch = branch


    def _get_template(template):
        if template is None:
            return self.template
        else:
            return template
    
    def init(self):
        self.repo.init()

    def commit(self, content, template=None):
        template = get_template(template)
        self.repo.commit(m=template.fill(content))

    def reset(self):
        self.repo.reset('HEAD~1', soft=True)

    def push(self):
        self.repo.push('origin', self.branch)

    def read(self, from_date, to_date):
        self.repo.log()



