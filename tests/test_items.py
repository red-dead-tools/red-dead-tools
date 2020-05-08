from pathlib import Path

from red_dead.items import parse_data


test_dir = Path(__file__).parent
snapshot_path = test_dir / 'items.snapshot'


def get_snapshot():
    collections, items = parse_data()
    return '\n\n'.join([
        '\n'.join(map(str, sorted(collections))),
        '\n'.join(map(str, sorted(items)))
    ])


def test_snapshot_matches():
    expected = snapshot_path.read_text()
    assert get_snapshot() == expected


if __name__ == '__main__':
    snapshot = get_snapshot()
    snapshot_path.write_text(snapshot)
