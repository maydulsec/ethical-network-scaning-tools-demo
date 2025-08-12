#!/usr/bin/env python3
"""
localhost_port_checker.py
SAFE demo: only scans 127.0.0.1 or ::1. Designed for learning.
Do NOT modify to scan external IPs.
"""
import socket
import argparse
from typing import List

def check_port(host: str, port: int, timeout: float = 0.5) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            s.connect((host, port))
            return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False

def parse_ports(s: str) -> List[int]:
    parts = []
    for token in s.split(','):
        token = token.strip()
        if '-' in token:
            a,b = token.split('-',1)
            parts.extend(range(int(a), int(b)+1))
        elif token:
            parts.append(int(token))
    return sorted(set(parts))

def main():
    parser = argparse.ArgumentParser(description="Safe localhost port checker (localhost-only).")
    parser.add_argument('--host', default='127.0.0.1', choices=['127.0.0.1', 'localhost', '::1'],
                        help='Host to check (restricted to localhost addresses).')
    parser.add_argument('--ports', default='22,80,443', help='Comma-separated ports or ranges, e.g. 22,80,8000-8010')
    args = parser.parse_args()

    host = args.host
    ports = parse_ports(args.ports)
    print(f"Checking {host} on ports: {ports}")
    for p in ports:
        open_ = check_port(host, p)
        status = "OPEN" if open_ else "closed"
        print(f"  {host}:{p} -> {status}")

if __name__ == '__main__':
    main()
