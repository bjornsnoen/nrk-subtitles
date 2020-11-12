""" Conftest """
import requests
import requests_cache

def pytest_runtest_setup(item):
    """ Install requests cache before tests run """
    requests_cache.install_cache('test-cache')
