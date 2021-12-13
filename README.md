# Sparse merkle tree in solidity

Optimised sparse merkle tree writen in solidity.

Key features:
- Size adjustments (function `increaseDepth` and `decreaseDepth`)
- Update elemnts - `O(log N)`
- Auto adjustment and index management using 2 functions `addToNextEmpty` and `removeAndRebase`

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
Median:   178060
Average:  181622
Min:      162165
Max:      321091

-- REMOVE --
Median:   100712
Average:  91263
Min:      58036
Max:      108890
```

### keccak256

```
$ HASH=keccak DEPTH=10 brownie run gas_stats

--- ADD ---
Median:   164999
Average:  168561
Min:      149104
Max:      308030

-- REMOVE --
Median:   88788
Average:  80981
Min:      58036
Max:      96966
```

### diagram

Generate nice image:

```
python diagram.py
```

![Gas usage](./plot.png)
