# CARP Report	

###### Lida Zhao  11611803

###### *School of Computer Science and Engineering*

###### *Southern University of Science and Technology*

###### *Email: 11611803@mail.sustc.edu.cn*

### 1. Preliminaries

​	This project is trying to design and implement heuristic search algorithms for solving the famous NP hard problem--CARP.

#### 1.1. Problem Description

​	CARP is the short form of Capacitated Arc Routing Problem. It can be described as follows: given a mixed graph G =(V, E, A), with a set of vertices denoted by V, a set of edges denoted by E and a set of arcs (i.e., directed edges) denoted by A, and there is a central depot vertex *dep* ∈ V, where a set of vehicles are based. Each edge is associated with a demand, two vertices and cost. A solution to the problem is a routing plan that consists of a number of routes for the vehicles, and the objective is to minimize the total cost of the routing plan subject to three constraints: first, each route starts and ends at the depot; second, each task is served in exactly once; The total demand of each route must not exceed the capacity Q.[1]

#### 1.2. Problem Applications

​	CARP is a kind of ARC routing problem, and it has many applications in daily life such as urban waste collection, post delivery, sanding or salting the streets[1], etc.

#### 1.3. Software

​	This project is written in Python using PyCharm. The libraries being used includes random, time, NumPy and Copy.

### 2. Methodology	

​	CARP is such a hard problem that need us to care about every details in the program. In this section, I will show the notations, data structures, and the details of the algorithm being used in the codes.

2.1. Representation and data structure

​	This project contains some main data need to maintain during the whole process: **info**, **req_edges**, **dis_map**. Also, here are some attached data needed in the program or will have a great influence on the performance.

- ***info***  *diction*: (key : value) = (name : information)<br />Store the basic information for each test case. such as name, capacity, vehicles number, etc. 
- ***req_edges***  *diction*: (key : value) = ((v1, v2) : (cost, demand))<br />Store all the edges that have demand. Using vertices as key, cost and demand as the value  
- ***dis_map***  *2-d array*<br />Store the shortest distance from each edge to all the other edges. Calculated by Floyd algorithm  
- ***s_ls/s_x***  *tuple*: (routes, cost)<br />s_ls stands for solution local search, s_x is the solution after cross over  
- ***psize***  *integer*<br />population size, set to 30  
- ***ubtrial***  *integer*<br />Maximum trials for generating initial solutions, set to 50  
- ***opsize***  *integer*<br />No. of offspring generated in each generation, set to 6* psize  
- ***p_ls***  *float*<br />Probability of carrying out local search, set to 0.2  
- ***time_limit***  *integer*<br />time limitation, set to 60 or 120  
- ***seed***  *integer*<br />random seed  
- ***pop/pop_t***  *array*<br />The whole population which carries both parents and children generation

2.2. Model design

​	There are infinity solutions in the solution space. Manage to find the local optima is of vital importance, because the best solution is among those local optima. We never solve problems by leaping, thus, I try to solve this problem step by step. The first step, using path scanning to get several feasible solution. Put all the solutions in to the population. The second step,  apply cross over to generate new generations from the population. The third step, randomly choose the solutions from the population and apply local search algorithms such as ******single insertion*, double insertion, *swap******, etc. In order to get the local optimal solution. 

2.3. Architecture

​	In this part, I will list all the function that I defined. I divide those functions in to three kinds. **Main functions** are the most important functions, they are used to imply algorithms. **Auxiliary functions** are like small tools to simplify the code structure in **Main functions**. **Assembling functions** do not have any algorithm, their only usage is to assemble several **Main functions** and help delivering data cross the .py files. Here, I will describe the algorithms in the **Main functions**, and the pseudo code will be included in next part. Only brief functional introduction will be given to the other two kind of functions.

- **Main functions**

- floyd:  Using Floyd algorithm to calculate the minimum distance between each nodes. Floyd algorithm is such a w

- path_scanning

- single_insertion

- double_insertion

- swap

- crossover

- MAENS

- **Auxiliary functions**

  | name                       | usage                                                        | name                     | usage                                                        |
  | -------------------------- | ------------------------------------------------------------ | ------------------------ | ------------------------------------------------------------ |
  | ***time_out***             | Calculate the time to determine if stop searching            | ***fullable***           | Used in Path scanning to see whether                         |
  | ***max_depot, min_depot*** | Two of the greedy algorithms: maximum or minimum the distance from the depot | ***get_dif_random***     | get a different random number                                |
  | ***max_ds, min_ds***       | Two of the greedy strategies: maximum or minimum the (demand/serve cost) | ***is_same_solution***   | determine whether two routes are the same routes             |
  | ***contains***             | determine whether a solution contains certain routes         | ***HFLC***               | "Half Far Low Close" is one of the greedy strategies that when load less than half, choose the further task from depot, when load more than half, vise versa. |
  | ***combine***              | Used in cross over. It will help combine two segments from two routes | ***generate_set***       | Change the solution into a set in order to avoid duplicate edge |
  | ***invert***               | switch the two vertices of a certain edge                    | ***cal_cost, cal_load*** | calculate the cost or the load of a route                    |

- Assembling functions

  - generate_solution
  - to_format
  - local_search
  - get_information

2.4. Detail of algorithm

### 3. Empirical Verification

### 4. References

[1] 	Tang, Ke , Y. Mei , and X. Yao . "Memetic Algorithm With Extended Neighborhood Search for Capacitated Arc Routing Problems." *IEEE Transactions on Evolutionary Computation*13.5(2009):1151-1166.
