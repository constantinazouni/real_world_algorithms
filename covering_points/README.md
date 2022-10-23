# Covering Points

You can find the assignment instructions [here](https://louridas.github.io/rwa/assignments/covering-points/)

## Run
```
python points_cover.py [-f] [-g] points_file
```
```-f``` (full exploration): instructs the program to find the best solution, examining as many subsets as needed. If it is not given, the program will execute the greedy algorithm

```-g``` (grid) :  instructs the program to find only lines that are horizontal or vertical. If it is not given, the program may use any lines that pass through the points.

```points_file``` : is the name of the file that contains the points we want to cover.

### Examples
You can run the following examples:
```
python points_cover.py example_1.txt
```
```
python points_cover.py -f -g example_1.txt
```
```
python points_cover.py -g example_2.txt
```
```
python points_cover.py -f -g example_2.txt
```
```
python points_cover.py -g example_3.txt
```
```
python points_cover.py -f -g example_3.txt
```