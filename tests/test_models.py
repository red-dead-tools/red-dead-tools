from red_dead.models import Settings
import json

from red_dead.items import get_item, base_dir


sample_item_settings_path = base_dir / 'sample-settings' / 'c-items.json'


def test_settings():
    expected_data = json.load(sample_item_settings_path.open())

    imp_item = get_item('Bone arrowhead', 'arrowhead')
    unimp_item = get_item('Eight of wands', 'wand')

    setttings = Settings(
        important_items=[imp_item],
        unimportant_items=[unimp_item],
    )

    assert setttings.as_export() == expected_data
