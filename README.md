# Sparse merkle tree in solidity

Optimised Sparse merkle tree writen in solidity.

Key features:
- Size adjustments (function ```increaseDepth``` and ```decreaseDepth```)
- Update elemnts - ```O(log N)```

## Instalation

Brownie

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Ganache

```
nvm install 14
nvm use @14
npm install ganache-cli
```

## Compile

```
brownie compile
```

## Run test

Run in different terminals

```
ganache-cli
```

And run test

```
brownie test
```

## Gas usage

```
brownie run spt
```