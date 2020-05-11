import pytest

from red_dead.items import path_originals


@pytest.mark.parametrize('cached_path, submod_path', path_originals.items())
def test_data_is_up_to_date(cached_path, submod_path):
    cached_data = cached_path.read_text()
    submod_data = submod_path.read_text()

    assert cached_data == submod_data
