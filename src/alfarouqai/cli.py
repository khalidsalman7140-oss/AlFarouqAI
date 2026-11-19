# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Small cross-platform command-line interface. JSON inputs are data, never code."""
from __future__ import annotations
import argparse
import json
import sys
from .client import Client
from .core import Config, AlFarouqError, __version__
from .dependencies import doctor, install_extra, installation_plan


def main(argv=None):
    parser = argparse.ArgumentParser(prog='alfarouq', description='AlFarouq AI — local-first unified Python tools')
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--config', help='Explicit JSON config file')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('capabilities')
    sub.add_parser('doctor')
    sub.add_parser('models')
    for command in ('run', 'plan'):
        p = sub.add_parser(command)
        p.add_argument('task' if command == 'run' else 'prompt')
        p.add_argument('--inputs', default='{}', help='JSON object with explicit input paths/parameters')
        if command == 'run':
            p.add_argument('--output', help='New JSON/CSV/MD/HTML/TXT report file')
    p = sub.add_parser('install-extra')
    p.add_argument('extra')
    p.add_argument('--environment', required=True)
    p.add_argument('--yes', action='store_true', help='Explicit consent to PyPI downloads in dedicated virtual environment')
    args = parser.parse_args(argv)
    try:
        client = Client(Config.load(args.config) if args.config else None)
        if args.command == 'capabilities':
            data = client.capabilities()
        elif args.command == 'models':
            from .models import inventory
            data = inventory()
        elif args.command == 'doctor':
            data = doctor()
        elif args.command == 'install-extra':
            data = install_extra(args.extra, args.environment, consent=True) if args.yes else installation_plan(args.extra, args.environment)
        else:
            inputs = json.loads(args.inputs)
            if not isinstance(inputs, dict):
                raise ValueError('--inputs must be a JSON object')
            if args.command == 'plan':
                data = client.plan(args.prompt, **inputs)
            else:
                result = client.run(args.task, **inputs)
                if args.output:
                    result.export(args.output)
                data = result.to_dict()
        print(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except (AlFarouqError, ValueError, OSError) as exc:
        print(json.dumps({'error': type(exc).__name__, 'message': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
