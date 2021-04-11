# Time_Travel_Search_Algorithms

## Project description

The goal in this project is to use AI search algorithms in the 3D space to reach from an initial location to a target location with the optimal shortest path under some constratins. The constraints for every fixed z are as following: 1)  the space is considered to be grid of points (x,y) such that the point (0,0) is the southwest corner of the grid and the agent can move to one of the eight neighboring grid locations, 2) there are some points in the space that let the agent to move bi-direcitally to the upper or lower layer, i.e., increase or decrease its z value. 

The program gets an input.txt file in which has the follwoing format, 

The first line shows which algorthim to use, A*, BFS, UCS. Second line consists of two integers showing the size of the grid, "W H". Third line shows the inital point in the format "z x y" where 0<= x <= W-1 and 0<= y <= H-1 . Forth line is the target location in the same format as inital point location. Fifth line is an inter N, indicationg the number of connecting channels among differetn layers in space. Next N line consisits of these channel in the format "z1 x y z2", which shows there is a bi-directioanl channel between layer z1 and z2 at point (x,y).

The program will output a text file showing the moves agent needs to take, total number of steps the agent takes and the resuling total cost. 
