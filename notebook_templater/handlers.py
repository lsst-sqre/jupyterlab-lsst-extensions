"""
This is a Handler Module with all the individual handlers for LSSTQuery
"""
import json
import os
from jinja2 import Template
from notebook.utils import url_path_join as ujoin
from notebook.base.handlers import APIHandler

NBTEMPLATE = '''
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\\n",
    "token = os.getenv(\\"JUPYTERHUB_API_TOKEN\\")\\n",
    "print(\\"Placeholder for Butler query '{{query_id}}'\\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "LSST_Stack (Python 3)",
   "language": "python",
   "name": "lsst_stack"
  },
  "language_info": {
   "name": ""
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}'''.strip()


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
        query_id = post_data["query_id"]
        self.log.debug(query_id)
        result = self._substitute_query(query_id)
        self.finish(json.dumps(result))

    def _substitute_query(self, query_id):
        top = os.environ.get("JUPYTERHUB_SERVICE_PREFIX")
        root = os.environ.get("HOME")
        fname = self._get_filename(query_id)
        fpath = "notebooks/queries/" + fname
        os.makedirs(root + "/notebooks/queries", exist_ok=True)
        filename = root + "/" + fpath
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                body = f.read().decode("utf-8")
        else:
            with open(filename, "wb") as f:
                templatestr = self._get_template()
                template = Template(templatestr)
                body = template.render(query_id=query_id)
                f.write(bytes(body, 'utf-8'))
        retval = {
            "status": 200,
            "filename": filename,
            "path": fpath,
            "url": top + "/tree/" + fpath,
            "body": body
        }
        return retval

    def _get_filename(self, query_id):
        fname = "query-" + str(query_id) + ".ipynb"
        return fname

    def _get_template(self):
        # replace with call to template service
        return NBTEMPLATE


def setup_handlers(web_app):
    """
    Function used to setup all the handlers used.
    """
    # add the baseurl to our paths
    host_pattern = '.*$'
    base_url = web_app.settings['base_url']
    handlers = [(ujoin(base_url, r'/lsstquery'), LSSTQuery_handler)]
    web_app.add_handlers(host_pattern, handlers)
