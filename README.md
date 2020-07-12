# Simulation of Multi-Server Queuing Model
* This repository contians code for simulating a markovian multi-server queuing model (i.e. **M/M/s:FCFS/∞/∞**)
* This is my submission to the assignment for the course Operations Research (MATH F242) offered 2nd semester 2019-2020 at BITS Pilani, Pilani Campus.

## Use 
* Run ```python3 simulate.py```.
* Enter the time (in seconds) for simulation.
* Enter **ⲗ**, the Poisson distribution parameter for arrival of customers.
* Enter the number of servers **s**.
* Enter **μ**, the mean service rate for each server. Thus, service time is exponentially distributed with parameter **μ**.

## Notes
* The arrival of customers is independent of the service of customers.
* The queue length is infinite.
* The population of customers is infinite.
* Servers are assigned customers in decreasing order of their speed (service rate)