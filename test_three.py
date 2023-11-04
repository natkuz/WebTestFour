import pytest
from BaseApp import BaseRestApi, BaseSoapApi
import yaml

with open('testdata.yaml', encoding='utf-8') as f:
    data = yaml.safe_load(f)


def test_step_one(coordinates, text_search):
    assert text_search in BaseRestApi.get_sites(coordinates[0], coordinates[1], 100, 100), "not found"


def test_step_two():
    assert 'молоко' in BaseSoapApi.check_text('малако'), 'test_step_one FAIL'


if __name__ == '__main__':
    pytest.main(['-vv'])
