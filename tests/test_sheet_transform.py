from red_dead.sheet_transform import get_col_item_needs, get_rows


def test_sheet_headings():
    expected_collections = {
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
    rows = get_rows()
    collections = set(get_col_item_needs(rows))
    assert collections == expected_collections
