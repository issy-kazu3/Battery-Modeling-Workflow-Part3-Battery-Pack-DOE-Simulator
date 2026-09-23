# Battery-Modeling-Workflow-Part3-Battery-Pack-DOE-Simulator

A Python-based Design of Experiments (DOE) tool for battery pack architecture exploration.

This project is the third step of a battery simulation workflow:

- Part-1 : Cell parameter identification from raw measurement data

- Part-2 : Battery energy flow simulation

- Part-3 : DOE-based battery pack design exploration (this repository)

The DOE engine automatically generates series-parallel pack configurations, evaluates battery pack performance using the energy flow simulator, and identifies feasible designs satisfying voltage, energy, and weight constraints.

![DOE](https://github.com/issy-kazu3/Battery-Modeling-Workflow-Part3-Battery-Pack-DOE-Simulator/blob/main/image/overview_of_DOE.png)

## Concept

Instead of evaluating a single battery pack design, this tool explores an entire design space.

For each combination of:

- Number of series cells
- Number of parallel cells
- Cell specification
- Voltage limits
- Energy requirements

the simulator evaluates feasibility and visualizes the resulting design space.

The objective is to uncover trade-offs between:

Pack weight
Voltage margin
Depth of discharge (DOD)
Battery configuration

## Workflow

Plain Text
DOE Input

│
▼

Energy Flow Simulator

│
▼
Pack Feasibility Evaluation
│
▼

Design Space Exploration

## Typical Results

The DOE analysis identifies:

- Feasible pack architectures
- Required series-parallel combinations
- Weight versus battery performance trade-offs
- Risk zones caused by excessive DOD
- Overdesigned regions with unnecessary pack mass

## Background

This repository is part of a Python-based battery engineering workflow developed as an open alternative to commercial DOE environments.

## Previous projects:

- Cell Parameter Identification : https://github.com/issy-kazu3/Battery-Modeling-Workflow-Part1-Parameter-Identification

- Battery Energy Flow Simulator : https://github.com/issy-kazu3/Battery-Modeling-Workflow-Part2-Battery-energy-simulation

The current repository extends these tools to system-level battery pack optimization and design space exploration.
