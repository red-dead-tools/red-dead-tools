from red_dead.sheet_transform import get_col_item_needs


def test_sheet_headings():
    expected_collections = {
        'Weekly',
        'Flowers',
        'Tarot Cards - Cups',
        'Tarot Cards - Swords',
        'Tarot Cards - Wands',
        'Tarot Cards - Pentacles',
        'Lost Jewelry - Bracelets',
        'Lost Jewelry - Earings',
        'Lost Jewelry - Necklaces',
        'Lost Jewelry - Rings',
        'Alcohol Bottles',
        'Egg',
        'Arrowheads',
        'Family Heirlooms',
        'Coins',
    }
    collections = set(get_col_item_needs())
    assert collections == expected_collections
