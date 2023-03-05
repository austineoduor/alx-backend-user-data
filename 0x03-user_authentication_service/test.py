#!/usr/bin/env python3
import bcrypt
password = b"super secret password"
# Hash a password for the first time, with a randomly-generated salt
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
# Check that an unhashed password matches one that has previously been
# hashed
if bcrypt.checkpw(password, hashed):
    print( hashed)
    print(password)
else:
    print("It Does not Match :(")
