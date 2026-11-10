"""Deterministic launch-only editorial preparation; never edits the catalogue.
Run without flags to preview, --write to apply, --check to validate the live file.
Episode subsequences and explicit reprise declarations are preserved per block.
"""
import argparse
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def prepare(config, catalog):
    result = deepcopy(config)
    if result.get('launchScheduleVersion') == 1:
        validate(result, catalog)
        return result
    by_id = {i['id']: i for i in catalog}
    original_episodes = [[i for i in b['rotation'] if by_id[i]['kind'] != 'short'] for b in result['blocks']]
    # Reuse all existing shorts before considering another verified daily play.
    # Keep the curated short-film and cinema sequences in place. Only episodic
    # blocks donate end-fillers to the shared pool for the new episode breaks.
    locked = {n for n, b in enumerate(result['blocks']) if sum(by_id[i]['kind'] == 'short' for i in b['rotation']) > len(b['rotation']) / 2}
    pool = [i for n, b in enumerate(result['blocks']) if n not in locked for i in b['rotation'] if by_id[i]['kind'] == 'short']
    counts = Counter(i for b in result['blocks'] for i in b['rotation'])
    result.update(continuityMode='block-opening-short-links', blockOpeningSeconds=18, programmeLinkSeconds=4)
    blocks = result['blocks']
    # Tightest episodic block first (the eight-episode encore); do not spend
    # its small verified shorts in a roomier daytime block.
    order = sorted(range(len(blocks)), key=lambda n: (sum(by_id[i]['durationSeconds'] for i in original_episodes[n]) / ((blocks[n + 1]['start'] if n + 1 < len(blocks) else result['cycleSeconds']) - blocks[n]['start'])), reverse=True)
    for n in order:
        block = blocks[n]
        if n in locked:
            continue
        block['rotation'] = []
        previous, run = None, 0
        for ident in original_episodes[n]:
            item = by_id[ident]
            series = item.get('series') if item['kind'] == 'episode' else None
            if series and series == previous and run == 2:
                # Smallest reusable short makes room for the whole episode sequence.
                chosen = min(pool, key=lambda i: (by_id[i]['durationSeconds'], i))
                pool.remove(chosen)
                block['rotation'].append(chosen)
                previous, run = None, 0
            block['rotation'].append(ident)
            run = run + 1 if series and series == previous else 1
            previous = series
    # Allocate existing shorts largest-first to retain every original play where feasible.
    for ident in sorted(pool, key=lambda i: (-by_id[i]['durationSeconds'], i)):
        candidates = [(remaining(result, n, by_id), n) for n in range(len(blocks))]
        candidates = [(r, n) for r, n in candidates if r >= by_id[ident]['durationSeconds'] + (4 if blocks[n]['rotation'] else 18) and (not blocks[n]['rotation'] or blocks[n]['rotation'][-1] != ident)]
        if not candidates:
            raise ValueError(f'Existing short does not fit without cutting a work: {ident}')
        _, n = max(candidates)
        blocks[n]['rotation'].append(ident)
    # Only fill residuals beyond 180s, within verified editorial caps.
    for n, block in enumerate(blocks):
        while remaining(result, n, by_id) > 180:
            room = remaining(result, n, by_id)
            candidates = [i for i in catalog if i['kind'] == 'short' and i.get('broadcastEnabled') is True
                          and i.get('verification', {}).get('status') == 'VERIFIED'
                          and i['verification'].get('actualPlayback') is True
                          and counts[i['id']] < i['editorialMaxDailyPlays']
                          and i['durationSeconds'] + 4 <= room
                          and i['id'] != block['rotation'][-1]]
            if not candidates:
                raise ValueError(f'Cannot safely fill {block["label"]}: {room}s')
            chosen = min(candidates, key=lambda i: (abs(room - i['durationSeconds'] - 4 - 90), counts[i['id']], i['id']))
            block['rotation'].append(chosen['id'])
            counts[chosen['id']] += 1
    result['launchScheduleVersion'] = 1
    for n, block in enumerate(blocks):
        assert [i for i in block['rotation'] if by_id[i]['kind'] != 'short'] == original_episodes[n]
    validate(result, catalog)
    return result


def remaining(config, index, by_id):
    block = config['blocks'][index]
    end = config['blocks'][index + 1]['start'] if index + 1 < len(config['blocks']) else config['cycleSeconds']
    ids = block['rotation']
    used = sum(by_id[i]['durationSeconds'] for i in ids) + (18 + 4 * (len(ids) - 1) if ids else 0)
    return end - block['start'] - used


def validate(config, catalog):
    by_id = {i['id']: i for i in catalog}
    counts = Counter()
    previous, run = None, 0
    for n, block in enumerate(config['blocks']):
        room = remaining(config, n, by_id)
        if not 0 <= room <= 180:
            raise ValueError(f'{block["label"]}: unsafe continuity {room}s')
        for ident in block['rotation']:
            item = by_id[ident]
            assert item.get('broadcastEnabled') is True and item['verification']['status'] == 'VERIFIED' and item['verification']['actualPlayback'] is True
            counts[ident] += 1
            series = item.get('series') if item['kind'] == 'episode' else None
            run = run + 1 if series and series == previous else 1
            previous = series
            assert run <= 2, f'{block["label"]}: series run {series}'
    for ident, count in counts.items():
        assert count <= by_id[ident]['editorialMaxDailyPlays'], f'{ident}: cap exceeded'
    for item in catalog:
        assert not item.get('broadcastEnabled') or counts[item['id']] > 0, f'{item["id"]}: missing enabled work'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    path = ROOT / 'data/schedule.json'
    config = json.loads(path.read_text(encoding='utf-8'))
    catalog = json.loads((ROOT / 'data/catalog.json').read_text(encoding='utf-8'))
    result = config if args.check else prepare(config, catalog)
    validate(result, catalog)
    if args.write:
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    by_id = {i['id']: i for i in catalog}
    print(json.dumps({'written': args.write, 'blocks': [{'label': b['label'], 'programmes': len(b['rotation']), 'continuitySeconds': remaining(result, n, by_id)} for n, b in enumerate(result['blocks'])]}, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()
