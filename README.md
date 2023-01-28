# CrackMyHash
## Multi-threaded brute-force application for cracking password hashes.

<p align="center">
<img src="imgs/logo.png" width="200">
</p>

## Features 
- Sha1 / Sha256 password cracking.
- Dictionary attack on a supplied hash.
- Use different modes - FULL / REGULAR / LIMITED, to decide the range of characters to try.

## Syntax examples
- python3 crackmyhash.py -h
- python3 crackmyhash.py -u sha1 -v b80abc2feeb1e37c66477b0824ac046f9e2e84a0 -d dict/passwords.txt
- python3 crackmyhash.py -u sha256 -v a42404a554a3a1336d5e2602c884c4e6e49cb2fdc5c470442fe611adde10192f -m LIMITED

<p align="center">
<img src="screenshots/s.png" width="700">
</p>
