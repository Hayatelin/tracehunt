#! /usr/bin/env python3

"""
TraceHunt: Find Usernames Across Social Networks Module

This module contains the main logic to search for usernames at social
networks.
"""

import sys


if __name__ == "__main__":
    # Check if the user is using the correct version of Python
    python_version = sys.version.split()[0]

    if sys.version_info < (3, 9):
        print(f"TraceHunt requires Python 3.9+\nYou are using Python {python_version}, which is not supported by TraceHunt.")
        sys.exit(1)

    from tracehunt import core
    core.main()
