# 🍪 Biscuit Optimization

The **Biscuit Optimization** project aims to maximize the profit of a biscuit manufacturing process by optimizing the placement of biscuits on a continuous dough strip. This project involves solving a complex optimization problem where various biscuits with different sizes and values need to be placed efficiently while avoiding defective areas on the dough.

---

## 📋 Project Overview

In the biscuit manufacturing industry, efficient use of the dough is critical to **minimize waste** and **maximize profit**. This project tackles the optimization challenge by:

- Identifying and handling defects on the dough strip.
- Selecting and placing biscuits based on their size and profit potential.
- Balancing the trade-off between maximizing the number of biscuits placed and minimizing empty spaces.

The solution employs **heuristic algorithms** and custom optimization strategies to achieve an optimal placement configuration.

---

## 🛠️ Technologies Used

- **Programming Language**: Python
- **Libraries**: OR-Tools, NumPy, Matplotlib (for data visualization)
- **Optimization Techniques**: Genetic Algorithms, Greedy Search, Constraint Satisfaction Problem (CSP), Dynamic Programming (DP)

---

## 🧩 Project Structure

The project is organized into several key classes:

- **`Biscuit`**: Represents a biscuit with attributes such as name, length, value, and defect thresholds.
- **`Dough`**: Represents the dough strip, managing defects and biscuit placement.
- **Genetic Algorithm Variants**:
  - **`GeneticAlgorithm`**: Basic genetic algorithm with selection, crossover, and mutation.
  - **`GeneticElitism`**: Genetic algorithm with elitism to retain top individuals.
  - **`GeneticTournament`**: Genetic algorithm using tournament selection.
  - **`UniformCrossoverGA`**: Genetic algorithm with uniform crossover.
- **Other Modules**:
  - **`main.py`**: Main script to execute the optimization processes.

---

## ⚙️ Methodology

The optimization process follows these steps:

### 1. Data Preparation

- **Load defect data** from CSV files, specifying defect positions and classes (e.g., `a`, `b`, `c`).
- **Segment the dough strip** into chunks, each represented by a `Chunk` object.

### 2. Defect Analysis

- Identify defective areas on the dough based on defect data.
- Assign defect classes to chunks, with the ability to handle overlapping defects.

### 3. Biscuit Placement Strategy

- **Prioritize biscuits** based on different heuristics:
  - **Value Heuristic**: Highest value.
  - **Value/Length Heuristic**: Best value-to-length ratio.
  - **Value/(Length \* Max Defects)**: Value relative to length and defect thresholds.
- Implement a **chunk-based analysis** to find the optimal placement for each biscuit.
- Track empty chunks and adjust the profit calculation accordingly.

### 4. 📊 Evaluation

- Calculate the **total profit** based on the placed biscuits and the cost of empty spaces.
- Evaluate the performance of different heuristics and optimization methods.

---

## 🧪 Results

The heuristic and AI-based approaches yielded the following results:

| **Approach**                                      | **Result** |
|---------------------------------------------------|------------|
| Basic Genetic Algorithm                           | 613        |
| Genetic Algorithm with Elitism                   | 630        |
| Genetic Algorithm with Tournament Selection      | 639        |
| Genetic Algorithm with Uniform Crossover         | 640        |
| Greedy Search with Value Heuristic               | 675        |
| Greedy Search with Value/Length Heuristic        | 690        |
| Greedy Search with Value/(Length \* Max Defects) | 672        |
| CSP with OR-Tools                                | 715        |
| Dynamic Programming                              | 715        |

### Key Insights

- **CSP and Dynamic Programming** achieved the best results (715) by providing optimal solutions.
- **Greedy Search** with the **Value/Length Heuristic** was fast and effective, achieving a score of 690.
- **Genetic Algorithms** provided competitive solutions but required careful tuning of parameters and were more computationally intensive.


