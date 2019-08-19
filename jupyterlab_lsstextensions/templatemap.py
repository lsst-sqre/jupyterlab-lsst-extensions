"""
This defines a git repository for each known query_type.
"""

TEMPLATEMAP = {
    "api": {"url": "https://something",
            "branch": "master",
            "subdir": None},
    "squash": {"url": "https://github.com/lsst-sqre/squash-bokeh",
               "branch": "master",
               "subdir": "template_notebooks/check_astrometry"}
}
