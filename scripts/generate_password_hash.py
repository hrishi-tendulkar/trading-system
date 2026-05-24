#!/usr/bin/env python3

from __future__ import annotations

import getpass

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def main() -> None:
    password = getpass.getpass("Shared site password: ")
    confirm = getpass.getpass("Confirm password: ")
    if password != confirm:
        raise SystemExit("Passwords did not match.")
    print(pwd_context.hash(password))


if __name__ == "__main__":
    main()
