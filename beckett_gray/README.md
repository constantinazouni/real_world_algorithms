# Beckett-Gray

You can find the assignment instructions [here](https://louridas.github.io/rwa/assignments/samuel-beckett-and-gray-codes/)

## Run
```
python beckett_gray.py [-a | -b | -u | -c | -p] [-r] [-f] [-m] number_of_bits
```

`-a`: find all codes (cycles and paths)

`-b`: find Beckett-Gray codes

`-u`: find Beckett-Gray paths (not cyles)

`-c`: find cyclical codes

`-p`: find Gray paths

`-r`: find reverse isomorphisms

`-f`: show the full binary representation of each code

`-m`: show each code with a tabular representation

`number_of_bits`: the number of bits of the code

### Examples
You can run the following examples:
```
python beckett_gray.py -a 3
```
or simply
```
python beckett_gray.py 3
```
```
python beckett_gray.py -b 5
```
```
python beckett_gray.py -b 5 -r
```
```
python beckett_gray.py -c 4
```
```
python beckett_gray.py -u 3
```
```
python beckett_gray.py -u 4
```
```
python beckett_gray.py -b -f 5
```
```
python beckett_gray.py -u -m 4
```