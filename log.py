from BehaviorAssistant.git import GitRepo
import dateutil.parser.parse

class LogEntry(object):
    def __init__(self, commit_id=None, author=None, datetime=None, content_dict=None, message=''):
        self.commit_id = commit_id
        self.content_dict = content_dict
        self.datetime = datetime
        self.message = message


class Log(object):

    def __init__(self, repopath, branch, template, config):
        self.repo = GitRepo.factory(repopath)
        self.template = template
        self.branch = branch
        self.config = config


    def _get_template(template):
        if template is None:
            return self.template
        else:
            return template
    
    def init(self):
        self.repo.init()

    def commit(self, content_dict, template=None):
        template = get_template(template)
        self.repo.commit(m=template.fill(content_dict))

    def reset(self):
        self.repo.reset('HEAD~1', soft=True)

    def push(self):
        self.repo.push('origin', self.branch)

    def read(self, since, until):
        log_entries = []
        log_entry = None
        output = self.repo.log(since=since, until=until)
        for line in output.split('\n'):
            fields = line.split(':')
            preamble = fields[0].strip()
            if preamble[:6] == 'commit':
                if log_entry is not None and not self.config.filter_ignore(log_entry):
                    log_entries.append(log_entry)
                log_entry = LogEntry(commit_id=fields[1].strip())
            elif preamble == 'Author':
                log_entry.author = fields[1].strip()
            elif preamble == 'Date':
                log_entry.datetime = dateutil.parser.parse(fields[1].strip())
            else:
                if '[ba]' in line:
                    # This means it's ba markup
                    content_name, content_value = line.replace('[ba]', '').split(':')
                    content_value = content_value.split()
                    log_entry.content_dict[content_name] = content_value
                else:
                    # This means it's just a regular commit or optional message
                    log_entry.message += line

        if log_entry is not None and not self.config.filter_ignore(log_entry):
            log_entries.append(log_entry)

        return log_entries



