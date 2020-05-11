from red_dead import base_dir
from red_dead.items import parse_data


snapshot_path = base_dir / 'tests/items.snapshot'


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
    print(f'Snapshot written to {snapshot_path}')
