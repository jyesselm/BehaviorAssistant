
import os

#BA modules 

class ConfigFileParser(object):
	def parse(self,file_path,warnings=0):
		options = {}

		try:
			f = open(file_path)
			lines = f.readlines() 
			f.close()
		except:
			if warnings:
				print "WARNING ConfigFileParser::parse cannot open config file ",file_path
			return options

		for l in lines:
			spl = l.split("=")
			if len(spl) != 2:
				print "WARNING ConfigFileParser::parse in config file",file_path,"line: ",l,"not correctly formated"
				continue 
			options[spl[0].rstrip().lstrip()] = spl[1].rstrip().lstrip()

		return options

class Configurations(object):
	def __init__(self):
		self.options = self._get_default_options()
		self.file_parser = ConfigFileParser()

	def parse_file(self,file_path):
		options = self.file_parser.parse(file_path)
		self.set_new_options(options)

	def set_new_options(self,options):
		for k,v in options.iteritems():
			if k not in options:
				print "WARNING Configurations::_set_new_options option",k,"not a valid option skipping..."
				continue
			self.options[k]=v

	def _get_default_options(self):
		options = {
			'git_repo'      : '.',
			'get_log_repo'  : '.',
			'program'		: None,
			'files'			: []
		}

		return options




def get_configurations(current_path):
	configs = Configurations()
	configs.parse_file(current_path + "/.ba_config")

	return configs







