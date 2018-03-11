# FOREX1
Forex Analysis - Arbitrage

Introduction of the project 

Foreign Currency exchange analysis based on Bellman-Ford modelling of real-time FOREX exchange data seeking triangular arbitrage opportunities comprising three modules (data sourcing/compiling, Bellman-Ford analysis/output, Forex trade activation)

The specification about the software

Module 1:  Forex data sourcing/compiling

Acquire real-time forex data from 1Forge (https://1forge.com/forex-data-api) and manipulate it as required into format necessary for module 2.

Module 2: Bellman-Ford analysis/output

Undertake analysis of forex data to find a shortest path between two nodes in a given graph either with Dijkstra’s algorithm or Bellman-Ford algorithm. Usually Dijkstra’s approach is better, but Bellman-Ford method is more robust. It can handle negative edge weights as well. Using a table of exchange rates, the program will have to construct a graph out of the table. The nodes of the graph will be the currencies. The edges represent the relationship between the currencies: it will be a fully connected graph based on exchange rates.  The output will be negative weighted sequence of forex orders suitable for ordering.

Module 3: Forex trade activation

When opportunities are identified in Module 2, it will utilize high-frequency forex trading firms, such as Kantox (https://www.kantox.com/en/), to place orders that can be repeatedly executed for as long as the arbitrage opportunity exists.  Once the opportunity closes, the program will revert to Module 1 and repeat until directed to cease.   

Functional Requirements

Module 1:
Import real-time API forex data and compile into an array/graph for use in Module 2

Module 2:
Analysis of multi-nodal Bellman-Ford algorithm to ascertain sequencing suitable to undertake automated orders in Module 3

Module 3: 
Place orders and assess relative output for errors (i.e. the trades are producing positive currency growth rather than negative growth).  If yes, and opportunity still exists, re-execute the sequence, check for positive growth and repeat. 

Non functional requirements 

Unknown?

Numbers of inputs that the program would need and under what format they will be 

API data is available for 134 foreign currencies but it is unclear which currencies are actively traded and thus the number of inputs may be reduced to less than 50.

Sample of output that you think the software would output you 

Module 1:
See table 1 at http://www.globalsoftwaresupport.com/forex-arbitrage-bellman-ford/

Module 2:
Arbitrage opportunity exists:
CDN 
EUR
JPN
USD
CDN
Potential opportunity ($25000): $63.51

Module 3:
Executed trades with error reporting via text message with automatic trading cessation.

Functions that you think can be divided in the program and their functionality 

See above

What kind of API (not that important for now but will be useful for later)

See above

Information sample that could be needed to run it (Fake data)

See table 1 at http://www.globalsoftwaresupport.com/forex-arbitrage-bellman-ford/
