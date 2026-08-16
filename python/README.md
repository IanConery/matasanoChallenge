# Python solutions

One file per challenge under `setNN/`, shared helpers in `lib/`.

## Setup

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Running

```sh
.venv/bin/python set01/ch01.py
```

Each script prints its result and asserts a known answer before printing `OK`.

## Notes

- AES/SHA primitives come from `pycryptodome` (see `requirements.txt`).
- Challenges whose "server" is specified by the challenge text (oracles)
  implement the oracle locally and attack it.
- `from_scratch/` holds hand-rolled primitives, to be filled in as needed.
