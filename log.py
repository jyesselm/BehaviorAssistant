import copy
import notifications
import shutil
from git import GitRepo
import time
import os
import dateutil.parser

class Content(object):
    @staticmethod
    def generate_content_dict(config, **kwargs):
        # would be nice to have some asserts here...
        content_dict = {}
        for arg_name, arg_val in kwargs.iteritems():
            if not config.check_if_ignore(arg_name):
                content_dict[arg_name] = arg_val
        return content_dict

class LogEntry(object):
    def __init__(self, commit_id=None, author=None, datetime=None, content_dict=None, message=""):
        self.commit_id = commit_id
        if content_dict == None:
            self.content_dict = {}
        else:
            self.content_dict = content_dict
        self.datetime = datetime
        self.message = message


class Log(object):

    BA_TAG = "[ba]"

    def __init__(self, config):
        self.config = config
        self.repo = GitRepo.factory(self.config.general_options["git_repo"])
        self.log_dir = self.config.general_options["git_repo"] + "/balog"
        if not os.path.isdir(self.log_dir):
            os.mkdir(self.log_dir)

    def get_output_log_dir(self):
        #TODO Sleep to avoid clashes if this directory exists and print
        # warnings..
        return self.log_dir + "/" + time.strftime("%Y.%m.%d.%H.%M.%S")


    def _get_template(command, template):
        if template is None:
            return self.config.get_command_template(command)
        else:
            return template
    
    def init(self):
        self.repo.init()
 
    def content_dict_str(self, content_dict):
        out_str = ""
        if "message" in content_dict:
            out_str += content_dict["message"] + "\n"
        for name, content in content_dict.iteritems():
            if name == "message":
                continue
            out_str += "%s %s:%s\n" % (Log.BA_TAG, name, content)
        return out_str

    def commit(self, command, command_args, message, stdout, stderr, command_run_time=None):
        """ Commits command and command_args with a message, stdout, and stderr
         Returns if we need a push
        """
        output_log_dir = self.get_output_log_dir()
        content_dict = Content.generate_content_dict(self.config, command=command, command_args=command_args, message=message, stdout=stdout, stderr=stderr, resource_dir=output_log_dir)
        self.repo.add("-A")
        #TODO setup proper tmp file
        commitfile = open("tmp.txt", "w")
        commitfile.write(self.content_dict_str(content_dict))
        commitfile.close()
        self.repo.commit(F="tmp.txt", a=True)

        commit_id = self.repo.log(format="%H", n=1)
        notifications.show("Logging in git log and %s" % output_log_dir)
        t0 = time.clock()
        command_header = "%s\n%s %s\n" % (commit_id, command, command_args)

        if not os.path.exists(output_log_dir):
            os.mkdir(output_log_dir)

        outfile = open(output_log_dir + "/out", "a")
        outfile.write(command_header)
        outfile.write(stdout)
        outfile.close()

        errfile = open(output_log_dir + "/err", "a")
        errfile.write(command_header)
        errfile.write(stderr)
        errfile.close()
        
        if command_run_time is not None:
            statsfile = open(output_log_dir + "/stats", "a")
            statsfile.write(command_header)
            statsfile.write("time: " + str(time.clock() - command_run_time) + "\n")
            statsfile.close()


        return content_dict, self.config.check_if_needs_push()

    def move_resources_to_resource_dir(self, content_dict, template):
        for name, resource in template.get_resources().iteritems():
            shutil.copyfile(resource, content_dict["resource_dir"] + "/" + resource)

    def reset(self):
        self.repo.reset("HEAD~1", soft=True)

    def push(self):
        self.repo.push("origin", self.config.general_options["branch"])

    def get_file_by_commit(self, commit_id, filename, outdir):
        out = self.repo.show("%s:%s" % (commit_id, filename))
        outfile = open(outdir + "/" + filename + "_" + commit_id, "w")
        outfile.write(out)
        outfile.close()

    def _parse_line(self, line):
        fields = line.replace(Log.BA_TAG, "").split(":")
        #TODO better parsing, taking into account external colons
        return fields[0], ":".join(fields[1:])

    def read(self, since, until):
        log_entries = []
        log_entry = None
        #TODO until, also use the gitrepo object somehow
        output = os.popen("git --no-pager log --since "%s"" % since).read()
        for line in output.split("\n"):
            if len(line.strip()) == 0:
                continue
            fields = line.split(":")
            preamble = fields[0].strip()
            if preamble[:6] == "commit":
                if log_entry is not None and not self.config.filter_ignore(log_entry):
                    log_entries.append(log_entry)
                log_entry = LogEntry(commit_id=line.split()[1])
            elif preamble == "Author":
                log_entry.content_dict["author"] = [fields[1].strip()]
            elif preamble == "Date":
                date_str = ":".join(fields[1:]).strip()
                date_str = " ".join(date_str.split()[:-1])
                log_entry.content_dict["date"] = [dateutil.parser.parse(date_str)]
            else:
                if Log.BA_TAG in line:
                    # This means it"s ba markup
                    content_name, content_value = self._parse_line(line)
                    content_name = content_name.strip()
                    # TODO do we really want to do this stripping?
                    content_value = [x.strip() for x in content_value.split()]
                    log_entry.content_dict[content_name] = content_value
                else:
                    # This means it"s just a regular commit or optional message
                    if "message" not in log_entry.content_dict:
                        log_entry.content_dict["message"] = []
                    log_entry.content_dict["message"].append(line)

        if log_entry is not None and not self.config.filter_ignore(log_entry):
            log_entries.append(log_entry)

        return log_entries



