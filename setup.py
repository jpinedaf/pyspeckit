#!/usr/bin/env python

import os, shutil
import setuptools
from setuptools import setup

with open('README.txt') as file:
    long_description = file.read()

version_base="0.1.1"
tagname = "pyspeckit_%s" % (version_base)

if os.path.exists(".hg"):
    # if the installed version is from a mercurial clone, get the "tip", else get the latest release
    try:
        import subprocess
        currentversion = subprocess.Popen(["hg","id","--num"],stdout=subprocess.PIPE).communicate()[0].strip().strip("+")
        tags = subprocess.Popen(["hg","tags"],stdout=subprocess.PIPE).communicate()[0].split()
        tagdict = dict((tags[i],tags[i+1].split(':')) for i in range(0, len(tags), 2))
        tagdict.remove('tip')

        # set "default" to be the tip
        version = version_base+"hg"+currentversion
        download_url = "https://bitbucket.org/pyspeckit/pyspeckit.bitbucket.org/get/tip.tar.gz"

        # find out if current version matches any tags.  If so, set version to be that
        for k,v in tagdict.iteritems():
            if currentversion in v:
                version = k.strip("pyspeckit_")
                download_url = "https://bitbucket.org/pyspeckit/pyspeckit.bitbucket.org/get/%s.tar.gz" % (k)
    except:
        # is this bad practice?  I don't care if it's an import error, attribute error, or value error...
        version = version_base
        download_url = "https://bitbucket.org/pyspeckit/pyspeckit.bitbucket.org/get/%s.tar.gz" % (tagname)
else:
    version = version_base
    download_url = "https://bitbucket.org/pyspeckit/pyspeckit.bitbucket.org/get/%s.tar.gz" % (tagname)

setup(name='pyspeckit',
      version=version,
      description='Toolkit for fitting and manipulating spectroscopic data in python',
      long_description=long_description,
      author=['Adam Ginsburg','Jordan Mirocha'],
      author_email=['adam.g.ginsburg@gmail.com', 'mirochaj@gmail.com',
          'pyspeckit@gmail.com'], 
      url='https://pyspeckit.bitbucket.org/',
      download_url=download_url,
      packages=['pyspeckit', 'pyspeckit.spectrum', 'pyspeckit.spectrum.models',
          'pyspeckit.spectrum.readers', 'pyspeckit.spectrum.writers',
          'pyspeckit.spectrum.speclines', 'pyspeckit.cubes',
          'pyspeckit.wrappers','mpfit','parallel_map'],
      package_dir={'pyspeckit.spectrum.speclines':'pyspeckit/spectrum/speclines',
          'mpfit':'mpfit'}, 
      package_data={'pyspeckit.spectrum.speclines':['splatalogue.csv'],
          '':['pyspeckit/config_default']},
      include_package_data=True,
      requires=['matplotib','numpy'],
      classifiers=[
                   "Development Status :: 3 - Alpha",
                   "Programming Language :: Python",
                   "License :: OSI Approved :: MIT License",
                  ],
      
     )

# Copy default config file to directory $HOME/.pyspeckit
HOME = os.environ.get('HOME')
CWD = os.getcwd()
if not os.path.exists('%s/.pyspeckit' % HOME):
    os.mkdir('%s/.pyspeckit' % HOME)
    
if not os.path.exists('%s/.pyspeckit/config' % HOME):
    shutil.copyfile('%s/pyspeckit/config_default' % CWD, '%s/.pyspeckit/config' % HOME)
