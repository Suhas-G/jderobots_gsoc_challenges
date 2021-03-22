# Navigating Labrynth

Navigating the labrynth using only C++ STL

Tested on Ubuntu LTS 20.04 - g++ 9.3.0, GNU Make 4.2.1

## Structure
* main.cpp - This is the main application source file
* Makefile - Makefile for the application. The commands are
    * make clean - Clean the text files inside [output](./output) and also remove the executable generated from main.cpp
    * make all - Compile the project
    * make run - Clean the output files, compile and run the main.out with 3 sample data present in [sample](./sample)
* sample - Folder which has 3 samples of inputs
* output - Output folder where result is written into

## Running
```bash
make run
```
Output:
```bash
rm -f main.out
rm -f output/*
g++ main.cpp -o main.out
Running sample 1
./main.out sample/labrynth-1.txt output/output-1.txt
Running sample 2
./main.out sample/labrynth-2.txt output/output-2.txt
Running sample 3
./main.out sample/labrynth-3.txt output/output-3.txt
```

## Sample

Input:
```
##.##.#
#..##.#
#.#####
#..####
#######
```

Output:
```
6
##0##.#
#21##.#
#3#####
#45####
#######
```