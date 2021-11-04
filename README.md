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
Median:   178003
Average:  181565
Min:      162108
Max:      321034

-- REMOVE --
Median:   100703
Average:  91255
Min:      58031
Max:      108881
```

### keccak256

```
$ HASH=keccak DEPTH=10 brownie run gas_stats

--- ADD ---
Median:   164855
Average:  168417
Min:      148960
Max:      307886

-- REMOVE --
Median:   88779
Average:  80972
Min:      58031
Max:      96957
```

### diagram

Generate nice image:

```
python diagram.py
```

![Gas usage](./plot.png)
