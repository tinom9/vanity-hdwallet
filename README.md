# Vanity hierarchical deterministic wallet generator

Create wallets that derive vanity addresses for Ethereum, Bitcoin, and Cosmos
blockchains.

## Requirements

`python=^3.10` and `uv` are required to run this project.

## Set-up

Virtual environment has to be set-up.

```bash
uv sync
```

## CLI Usage

```bash
uv run cli.py generate -v abc123 -c ETH -l spanish -w 24 --case-sensitive
uv run cli.py multigenerate -v abc123,xyz -c ETH,BTC
```
