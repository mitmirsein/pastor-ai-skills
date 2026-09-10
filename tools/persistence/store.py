#!/usr/bin/env python3
"""Apply reviewed UTF-8 file replacements, with resumable per-file receipts."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


def target(root, relative):
    p = Path(relative)
    if p.is_absolute() or '..' in p.parts or not p.parts:
        raise ValueError('relative path required')
    resolved = (root / p).resolve()
    if not resolved.is_relative_to(root) or resolved == root:
        raise ValueError('path outside workspace')
    return resolved


def current_hash(path):
    return digest(path.read_bytes()) if path.exists() else None


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.save-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def apply(root, plan, fail_after=None):
    """Order must be artifact, manifest, indexes, journal. Never rebase stale plans."""
    root = Path(root).resolve(strict=True)
    op = plan['operation_id']
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', op):
        raise ValueError('invalid operation_id')
    entries = plan['writes']
    if not entries:
        raise ValueError('empty writes')
    paths = [target(root, e['path']) for e in entries]
    if len(set(paths)) != len(paths):
        raise ValueError('duplicate target')
    operation_dir = target(root, 'outputs/.operations')
    if any(p == operation_dir or p.is_relative_to(operation_dir) for p in paths):
        raise ValueError('operation receipts cannot be targets')
    for e in entries:
        if not isinstance(e['content'], str):
            raise ValueError('content must be UTF-8 text')
        before = e['before_sha256']
        if before is not None and not re.fullmatch('[0-9a-f]{64}', before):
            raise ValueError('invalid before_sha256')
        if e.get('kind') == 'artifact' and before is not None:
            raise ValueError('artifact must be a new path')
    # Validate encoding before acquiring the lock; malformed Unicode must not strand it.
    fingerprint = digest(json.dumps(plan, sort_keys=True, ensure_ascii=False).encode('utf-8'))
    operation_dir.mkdir(parents=True, exist_ok=True)
    # A root-wide lock serializes cooperating writers, including distinct operations.
    lock = operation_dir / '.lock'
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(fd)
    receipt_path = operation_dir / (op + '.json')
    receipt = {'operation_id': op, 'plan_sha256': fingerprint, 'plan': plan,
               'completed': [], 'status': 'pending'}
    receipt_owned = False
    try:
        resuming = receipt_path.exists()
        if not resuming:
            for entry, path in zip(entries, paths):
                if entry.get('kind') == 'artifact' and path.exists():
                    raise ValueError('artifact path already exists: ' + entry['path'])
        if resuming:
            receipt = json.loads(receipt_path.read_text())
            if receipt['plan_sha256'] != fingerprint:
                raise ValueError('operation_id reused with different plan')
        atomic_write(receipt_path, json.dumps(receipt, ensure_ascii=False, indent=2).encode())
        receipt_owned = True
        for i, (e, path) in enumerate(zip(entries, paths)):
            data = e['content'].encode('utf-8')
            actual = current_hash(path)
            if actual != digest(data):
                if actual != e['before_sha256']:
                    raise ValueError('concurrent edit at ' + e['path'])
                if fail_after is not None and i >= fail_after:
                    raise OSError('injected write failure at ' + e['path'])
                # Resolve again to catch a changed parent link before each write.
                if target(root, e['path']) != path:
                    raise ValueError('target changed')
                atomic_write(path, data)
                if current_hash(path) != digest(data):
                    raise OSError('read-back mismatch at ' + e['path'])
            if e['path'] not in receipt['completed']:
                receipt['completed'].append(e['path'])
            atomic_write(receipt_path, json.dumps(receipt, ensure_ascii=False, indent=2).encode())
        receipt['status'] = 'complete'
        receipt.pop('error', None)
    except Exception as exc:
        # Preserve the existing receipt if this was an attempt to reuse its ID.
        if receipt_owned:
            receipt['status'] = 'partial' if receipt['completed'] else 'failed'
            receipt['error'] = str(exc)
            atomic_write(receipt_path, json.dumps(receipt, ensure_ascii=False, indent=2).encode())
        raise
    else:
        atomic_write(receipt_path, json.dumps(receipt, ensure_ascii=False, indent=2).encode())
        return receipt
    finally:
        lock.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    parser.add_argument('--plan', required=True)
    args = parser.parse_args()
    try:
        result = apply(args.root, json.loads(Path(args.plan).read_text()))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, str(exc) + '\n')
    print(json.dumps({'status': result['status'], 'completed': result['completed']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
