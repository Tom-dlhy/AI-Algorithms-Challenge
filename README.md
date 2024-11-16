# 🍪 Biscuit Optimization

The **Biscuit Optimization** project aims to maximize the profit of a biscuit manufacturing process by optimizing the placement of biscuits on a continuous dough strip. This project involves solving a complex optimization problem where various biscuits with different sizes and values need to be placed efficiently while avoiding defective areas on the dough.

## 📋 Project Overview

In the biscuit manufacturing industry, efficient use of the dough is critical to minimize waste and maximize profit. This project tackles the optimization challenge by:
- Identifying and handling defects on the dough strip.
- Selecting and placing biscuits based on their size and profit potential.
- Balancing the trade-off between maximizing the number of biscuits placed and minimizing empty spaces.

The solution employs heuristic algorithms and custom optimization strategies to achieve an optimal placement configuration.

## 🛠️ Technologies Used

- **Programming Language**: Python
- **Libraries**: Pandas, NumPy, Matplotlib (for data visualization)
- **Optimization Techniques**: Heuristic algorithms, profit maximization, chunk-based analysis

## 🧩 Project Structure

The project is organized into several key classes:

- **Biscuit**: Represents a biscuit with attributes such as `name`, `length`, `value`, and `defect_thresholds`.
- **Chunk**: Represents a segment of the dough strip, with information on its position, defects, and occupation status.
- **BiscuitOptimization**: Main class for running the optimization process, managing biscuits, chunks, and implementing the placement algorithm.

## ⚙️ Methodology

The optimization process follows these steps:

1. **Data Preparation**:
   - Load defect data from CSV files, specifying defect positions and classes (e.g., `a`, `b`, `c`).
   - Segment the dough strip into chunks, each represented by a `Chunk` object.

2. **Defect Analysis**:
   - Identify defective areas on the dough based on defect data.
   - Assign defect classes to chunks, with the ability to handle overlapping defects.

3. **Biscuit Placement Strategy**:
   - Prioritize biscuits based on profitability (size-to-value ratio) and defect thresholds.
   - Implement a chunk-based analysis to find the optimal placement for each biscuit.
   - Track empty chunks and adjust the profit calculation accordingly.

4. **Evaluation**:
   - Calculate the total profit based on the placed biscuits and the cost of empty spaces.
   - Evaluate the performance of different heuristics (e.g., prioritizing smaller biscuits or high-value biscuits).

## 🧪 Results

The heuristic approach yielded promising results:
- **Maximized profit** by efficiently placing high-value biscuits while avoiding defective areas.
- **Reduced waste** by minimizing the number of empty chunks on the dough strip.
- **Improved flexibility** by allowing adjustments to defect thresholds and biscuit prioritization strategies.
