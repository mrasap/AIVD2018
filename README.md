# AIVD2018

This is an attempt to solve the AIVD kerstpuzzel 2018 teaser.

The teaser can be found here: https://twitter.com/AIVD/status/1070617628891320320

Note: the space of possibilities is at around 10^12, hence an evolutionary strategy is necessary.


### Features
[X] Bruteforce the available paths (this turned out to be 2)   
[X] Bruteforce the string     
[X] Evolutionary strategy for the string, including:   
[X] Mutate function   
[X] Crossover function   
[X] Fitness function level 1 (compute_valid): all characters should fit in any given word of the dutch dictionary   
[X] Fitness function level 2 (compute_sensible): favor longer words   
[X] Adaptive mutate rate   
[X] Periodically start with completely new chromosomes to avoid local minimum   
[X] Apply elitism   
[X] Graph out the performance at the end   
[] Dynamic programming to find the optimal splitting of words   
