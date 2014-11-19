import template

class HTMLRender(object):
    
    def _get_default_html_template(self):
        #TODO have this in a separate file?
        html = "<html>"
        html += "{{ entries }}"
        html += "</html>"
        return html
    
    def _render_content(self, content_dict):
        html = ""
        for content_type, content in content_dict.iteritems():
            if template.Template.is_resource(content_type):
                # TODO should this be done elsewhere? also, not readable at all
                if "resource_dir" in content_dict:
                    content[0] = content_dict["resource_dir"][0] + "/" + content[0]

            #TODO better content parsing
            if content_type == "show":
                html += "<img src=%s/>\n" % " ".join(content)
            if content_type == "message":
                html += "<p>%s</p>" % " ".join(content)
            if content_type == "author":
                html += "<p><b>%s</b></p>\n" % " ".join(content)
            if content_type == "date":
                html += "<p><i>%s</i></p>\n" % " ".join([str(d) for d in content])
            if content_type == "command":
                html += "<p><h2>%s</h2></p>\n" % " ".join([str(d) for d in content])
            if content_type == "command_args":
                html += "<p><h3>%s</h3></p>\n" % " ".join([str(d) for d in content])

        return html



    def render(self, log_entries, configs):
        out = self._get_default_html_template()
        entries_html = ""

        for log_entry in log_entries:
            if "command" not in log_entry.content_dict:
                continue
            #TODO better parsing of command name, remove ./ elsewhere
            command = log_entry.content_dict["command"][0].strip("./")
            template = configs.templates[command]
            filtered_content = template.filter(log_entry.content_dict)
            entries_html += self._render_content(filtered_content)

        return out.replace("{{ entries }}", entries_html)
        


def get_renderer(renderer_type):
    renderers = {"html":HTMLRender}
    return renderers[renderer_type]()

