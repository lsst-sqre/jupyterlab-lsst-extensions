"""
This is a Handler Module with all the individual handlers for LSSTQuery
"""
import json
import os
from jinja2 import Template
from notebook.utils import url_path_join as ujoin
from notebook.base.handlers import APIHandler

import nbreport
import nbreport.templating as templ
import nbformat
from nbreport.repo import ReportRepo


class LSSTQuery_handler(APIHandler):
    """
    LSSTQuery Parent Handler.
    """
    @property
    def lsstquery(self):
        return self.settings['lsstquery']

    def post(self):
        """
        POST a queryID and get back a prepopulated notebook.
        """
        self.log.warning(self.request.body)
        post_data = json.loads(self.request.body.decode('utf-8'))
        # Do The Deed
        query_id = post_data["query_id"]
        query_type = post_data["query_type"]
        self.log.debug("Query_Type: {}".format(query_type))
        self.log.debug("Query_ID: {}".format(query_id))
        result = self._substitute_query(query_id)
        self.finish(json.dumps(result))

    def _substitute_query(self, query_type, query_id):
        top = os.environ.get("JUPYTERHUB_SERVICE_PREFIX")
        root = os.environ.get("HOME")
        fname = self._get_filename(query_type, query_id)
        fpath = "notebooks/queries/" + fname
        os.makedirs(root + "/notebooks/queries", exist_ok=True)
        filename = root + "/" + fpath
        retval = {
            "status": 404,
            "filename": filename,
            "path": fpath,
            "url": top + "/tree/" + fpath,
            "body": None
        }
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                body = f.read().decode("utf-8")
        else:
            template = self._get_template(query_type)
            extra_context = self._get_extra_context_(query_type, query_id)
            if template and extra_context:
                nb = repo.open_notebook()
                cc = repo._dirname + "/cookiecutter.json"
                lload = templ.load_template_environment
                context = lload(cc, extra_context=extra_context)
                rnb = templ.render_notebook(nb, *context)
                nbformat.write(rnb, filename)
            else:
                return retval
        retval["status"] = 200
        retval["body"] = body
        return retval

    def _get_filename(self, query_id, query_type):
        fname = "query-" + query_type + "-" + str(query_id) + ".ipynb"
        return fname

    def _get_template(self, query_type):
        if query_type == "api":
            template_url = "..."
        elif query_type == "squash":
            template_url = "..."
        else:
            return None
        template_dir = self._clone_repo(template_url)
        repo = ReportRepo(template_url)
        return repo

    def clone_repo(self, template_url):
        pass  # FIXME

    def get_extra_context(self, query_type, query_id):
        context = {}
        if query_type == "api":
            context = {"query_id": query_id}
        elif query_type == "squash":
            context = {"ci_id": query_id}
        else:
            pass
        return context


rnb = templ.render_notebook(nb, *context)
nbformat.write(rnb, 'test.ipynb')
return template


def setup_handlers(web_app):
    """
    Function used to setup all the handlers used.
    """
    # add the baseurl to our paths
    host_pattern = '.*$'
    base_url = web_app.settings['base_url']
    handlers = [(ujoin(base_url, r'/lsstquery'), LSSTQuery_handler)]
    web_app.add_handlers(host_pattern, handlers)


# I already cloned the repo and checked out the right branch

nb = repo.open_notebook()
context = templ.load_template_environment('repos/squash-bokeh/check_photometry/cookiecutter.json', extra_context={'ci_id': < value_from_dialog >})
rnb = templ.render_notebook(nb, *context)
nbformat.write(rnb, 'test.ipynb')
