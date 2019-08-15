"""
Python module to initialize Server Extension (& Notebook Extension?)
"""
from jupyterlab_lsstquery.handlers import setup_handlers


def _jupyter_server_extension_paths():
    """
    Function to declare Jupyter Server Extension Paths.
    """
    return [{
        'module': 'jupyterlab_lsstquery',
    }]


# def _jupyter_nbextension_paths():
#    """
#    Function to declare Jupyter Notebook Extension Paths.
#    """
#    return [{"section": "notebook", "dest": "jupyterlab_lsstquery"}]


def load_jupyter_server_extension(nbapp):
    """
    Function to load Jupyter Server Extension.
    """
    nbapp.log.info("Loading lsstquery server extension.")
    setup_handlers(nbapp.web_app)
