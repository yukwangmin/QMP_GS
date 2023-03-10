# QMP_GS

This repository includes Python codes and the results of the running used in the paper, "Quantum multi-programming for Grover's search" [(https://doi.org/10.1007/s11128-022-03793-2)](https://doi.org/10.1007/s11128-022-03793-2).


## Note for Qiskit version

We used Qiskit version 0.38.0. However, Qiskit version 0.39.0 was released on Oct. 13, 2022 (https://qiskit.org/documentation/release_notes.html).
A notable difference between the versions is qiskit.visualization.plot_histogram().
Until version 0.38.0, plot_histogram() function plots probabilities (https://qiskit.org/documentation/stable/0.38/stubs/qiskit.visualization.plot_histogram.html?highlight=plot_histogram#qiskit.visualization.plot_histogram). But after version 0.39.0, the function plots the counts of the measurement (https://qiskit.org/documentation/stubs/qiskit.visualization.plot_histogram.html?highlight=plot_histogram#qiskit.visualization.plot_histogram).
Therefore, when you run our code, your histogram generated by plot_histogram() function will have the counts instead of probabilities as shown in this repository.

