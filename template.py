from collections import OrderedDict
import copy

class Template(object):
    

    @staticmethod
    def is_resource(name):
        #TODO enumerate all resource names
        resource_names = ["show"]
        return name in resource_names


    def __init__(self):
        self.sections = OrderedDict()
        self.sections["resource_dir"] = []

    def add_section(self, fields):
        self.sections[fields[0]] = fields[1:]

    def get_resources(self):
        resources = {}
        for name, content in self.sections.iteritems():
            if Template.is_resource(name):
                resources[name] =  content[0]
        return resources

    def filter(self, content_dict):
        new_content_dict = OrderedDict()
        for section in self.sections:
            if section in content_dict:
                new_content_dict[section] = copy.deepcopy(content_dict[section])
            else:
                new_content_dict[section] = copy.deepcopy(self.sections[section])
        return new_content_dict
