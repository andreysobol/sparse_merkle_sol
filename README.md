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
python processor.py
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
brownie run sha_gas
```

Result (depth = `10`)

```
ADD
Median: 
177243
Average: 
180793.3046875
Min: 
161351
Max: 
320247

REMOVE
Median: 
100062
Average: 
90612.185546875
Min: 
57505
Max: 
108213
```

### keccak256

```
brownie run keccak_gas
```

Result (depth = `10`)

```
ADD
Median: 
164375
Average: 
167937.3046875
Min: 
148480
Max: 
307406

REMOVE
Median: 
88294
Average: 
80505.2197265625
Min: 
57669
Max: 
96472
```

### diagram

Generate nice image:

```
python diagram.py
```

![Gas usage](./plot.png)