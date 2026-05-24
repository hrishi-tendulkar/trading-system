#!/usr/bin/env python3

from __future__ import annotations

import bcrypt
import getpass


def main() -> None:
    password = getpass.getpass("Shared site password: ")
    confirm = getpass.getpass("Confirm password: ")
    if password != confirm:
        raise SystemExit("Passwords did not match.")
    print(bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"))


if __name__ == "__main__":
    main()
