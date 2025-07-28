# Development Mode (`--dev`)

You can run the game in **development mode** by passing the `--dev` flag when executing the script. This mode speeds up testing by skipping the intro sequence.

## How to run in development mode

```python
python main.py --dev
```

## Implementation example

The game checks for the `--dev` argument using Python’s `argparse` module:

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dev', action='store_true', help='Activate development mode')
args = parser.parse_args()
dev_mode = args.dev

if dev_mode:
    # Skip intro sequence or enable dev features
    print("Development mode activated: skipping intro...")
    # your code here to skip intro
else:
    # Normal game start
    pass
```
