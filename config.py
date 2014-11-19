
import os

#BA modules 
import template

class ConfigFileParser(object):


    def _parse_line_option(self, line, line_no, file_path):
        spl = [field.strip() for field in line.split("=")]
        if len(spl) != 2:
            raise ValueError("WARNING ConfigFileParser::parse in config file", file_path,"line: ", line_no," not correctly formated")
        return spl

    def _parse_template_option(self, line, line_no, file_path):
        spl = [field.strip() for field in line.split()]
        return spl

    def parse(self,file_path,warnings=0):
        general = {}
        commands = {}
        templates = {}
        ignores = []

        f = open(file_path)
        lines = f.readlines() 
        f.close()

        if warnings:
            print "WARNING ConfigFileParser::parse cannot open config file ",file_path
            return None

        curr_template = None
        curr_section = ""
        curr_section_name = ""
        for line_no, line in enumerate(lines):
            line = line.strip()
            if len(line) == 0 or line[0] == "#":
                continue

            if line[0] == "[":
                # This means we are openning a new section
                if curr_template is not None:
                    templates[curr_section_name] = curr_template
                    curr_template = None

                curr_section = line.strip("[]")
                if " " in curr_section:
                    # Means that the tag in this section has a name e.g. for command or template tags
                    curr_section, curr_section_name = curr_section.split()
                continue
           
            if curr_section == "ignore":
                ignores.append(line)

            if curr_section == "general":
                option, value = self._parse_line_option(line, line_no, file_path)
                general[option] = value

            if curr_section == "command":
                if not curr_section_name  in commands:
                    commands[curr_section_name] = {}
                option, value = self._parse_line_option(line, line_no, file_path)
                commands[curr_section_name][option] = value

            if curr_section == "template":
                if not curr_section_name in commands:
                    templates[curr_section_name] = {}
                fields = self._parse_template_option(line, line_no, file_path)
                if curr_template == None:
                    curr_template = template.Template()
                curr_template.add_section(fields)

        if curr_template is not None:
            templates[curr_section_name] = curr_template

        config = Configurations()
        config.update_options("general", general)
        config.update_options("template", templates)
        config.update_options("command", commands)
        config.update_options("ignore", ignores)

        return config

class Configurations(object):
    def __init__(self):
        self.general_options = self._get_default_general_options()
        self.ignores = set()
        self.templates = {}
        self.commands = {}

    def check_if_ignore(self, name):
        return name in self.ignores

    def get_command_template(self, command):
        return self.templates[command]

    def check_if_needs_push(self):
        #TODO
        return False

    def filter_ignore(self, log_entry):
        #TODO
        return False

    def update_options(self, option_type, new_options):
        if option_type == "general":
            self.general_options.update(new_options)
        elif option_type == "template":
            self.templates.update(new_options)
        elif option_type == "command":
            self.commands.update(new_options)
        elif option_type == "ignore":
            for name in new_options:
                self.ignores.add(name)
        else:
            raise ValueError("Unrecognized option type %s" % option_type)

    def _get_default_general_options(self):
        general_options = {
            "git_repo"      : ".",
            "get_log_repo"  : ".",
            "files"            : []
        }

        return general_options


def get_configurations(current_path):
    config_parser = ConfigFileParser()
    config = config_parser.parse(current_path + "/.ba_config")

    return config

