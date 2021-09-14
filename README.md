![Tests passed](https://github.com/UST-QuAntiL/Quokka/actions/workflows/test.yml/badge.svg)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/UST-QuAntiL/quokka/branch/main/graph/badge.svg?token=0GO5H9V7QC)](https://codecov.io/gh/UST-QuAntiL/quokka)

# Quokka - A quantum algorithm composition layer

API Specification at: http://127.0.0.1:5000/api/swagger-ui

### Developer Guide

Setup (exemplary for ubuntu 18.04): 
* ``git clone https://github.com/UST-QuAntiL/quokka.git`` 
* ``cd quokka``
* ``sudo -H pip install virtualenv`` (if you don't have virtualenv installed)
* ``virtualenv venv`` (create virtualenv named 'venv')
* ``source venv/bin/activate`` (enter virtualenv; in Windows systems activate might be in ``venv/Scripts``)
* ``pip install -r requirements.txt`` (install application requirements)

Execution:
* Run with: ``flask run``
* Test with: ``flask test``
* Coverage with: ``flask test --coverage``

Codestyle: ``black . OR FILE|DIRECTORY``

Update requirements with: ``pip freeze>requirements.txt``