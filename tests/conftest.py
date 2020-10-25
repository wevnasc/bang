import pytest

import os
from shutil import rmtree


@pytest.fixture()
def tmp_folder():
    temp_dir = './tmp/'
    os.makedirs(temp_dir)
    yield temp_dir
    rmtree(temp_dir)

@pytest.fixture()
def template_folder():
    template = './test-templates'
    os.makedirs(template)
    yield template
    rmtree(template)