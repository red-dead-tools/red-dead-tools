import json
import re

from red_dead import base_dir
from red_dead.items import get_item
from red_dead.models import Settings


sample_item_settings_path = base_dir / 'sample-settings' / 'c-items.json'


def test_settings():
    expected_data = json.load(sample_item_settings_path.open())

    imp_item = get_item('Bone arrowhead', 'arrowhead')
    unimp_item = get_item('Eight of wands', 'wand')

    setttings = Settings(important_items=[imp_item], unimportant_items=[unimp_item],)

    exported = setttings.as_export()

    for key in [
        'main.isMenuOpened',
        'importantItems',
        'amount.wands_eight',
        'collected.wands_eight',
        'version',
    ]:
        assert exported[key] == expected_data[key]
