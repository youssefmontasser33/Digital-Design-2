 Simulated-Annealing Cell Placement Tool


 This project purpose is to take an input file of details about cells , number of connections, and size of the site and based on it we get an output to show us the grid of a better replacement and its estimated wire lenght

 The input file format: (There is 1 space between each number)
 First Line: number of cells , then number of connections , then number of rows, then number of columns.
 Then there are number of lines which are equals to number of connections.
 Each of these lines has the following format: number of celss connectd, then each cells that are connected together


In this project we faces a challenge in the inital value of moves/temperature which indicates the number of moves to decrease the temperature , and the problem is that the number of moves is so huge when we deal with many cells like 200. We dealt with this problem by decreasing moves/temperature value by modifiying the equation

