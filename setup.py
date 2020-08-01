"""
Setup Module to setup Python Handlers for LSST query templating
"""
import setuptools

setuptools.setup(
    name="jupyterlab_lsstextensions",
    version="2.0.0",
    packages=setuptools.find_packages(),
    install_requires=["nbreport>=0.7.3", "notebook", ],
    package_data={"jupyterlab_lsstextensions": ["*"]},
)
