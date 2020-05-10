from red_dead import base_dir
from red_dead.items import data_path


submod_path = base_dir / 'RDR2CollectorsMap/langs/en.json'


def test_data_is_up_to_date():
    cached_data = data_path.read_text()
    submod_data = submod_path.read_text()

    assert cached_data == submod_data
