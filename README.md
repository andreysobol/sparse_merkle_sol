# Sparse merkle tree in solidity

Optimised sparse merkle tree writen in solidity.

Key features:
- Size adjustments (function `increaseDepth` and `decreaseDepth`)
- Update elemnts - `O(log N)`

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
./processor.py
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

### sha256

```
$ HASH=sha DEPTH=10 brownie run gas_stats

--- ADD ---
Median:  176784
Average: 180346
Min:     160889
Max:     319815

-- REMOVE --
Median:  99939
Average: 90539
Min:     57647
Max:     108117
```

### keccak256

```
$ HASH=keccak DEPTH=10 brownie run gas_stats

--- ADD ---
Median:  163973
Average: 167535
Min:     148078
Max:     307004

-- REMOVE --
Median:  87940
Average: 80200
Min:     57647
Max:     96118
```

### diagram

Generate nice image:

```
python diagram.py
```

![Gas usage](./plot.png)
