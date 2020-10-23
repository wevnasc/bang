import pytest

from os import mkdir
from shutil import rmtree


@pytest.fixture()
def temp_folder():
    mkdir('./tmp/')
    yield './tmp/'
    rmtree('./tmp/')