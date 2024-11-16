# PennyTrade  
**Current Version: v1.2 (in development)**  

## Purpose of this Project  
PennyTrade is a program designed to use optimized algorithmic structures and mathematically analyzed functions to simulate realistic stock market price behaviors. These simulations consider both the most recent news and user-defined variables.  

For each simulation, the program identifies optimal buy and sell points. While doing so, it generates mathematical functions that serve as the foundation for subsequent simulations. As the number of simulations increases, the algorithm improves its accuracy through iterative learning.  

The system not only analyzes current prices but also integrates and adapts to real-time news updates. The primary goal is not to generate profit but to develop algorithms capable of solving and modeling highly unpredictable and complex scenarios, similar to chess—but on an infinite board where a pawn can transform into a queen.  

---

## Features in Version 1.2  

### Simulation Features (C Code)  
- Generates a large number of simulations based on user-defined variables.  
- User-defined variables in this version include:  
  1. Number of price points to be generated.  
  2. Probability of price increase or decrease.  
  3. Price gap between points. (if set to 200 and initial point is 62200 next possible output either 62400 or 6200).
  4. Start date for price generation. 
  5. Name of the simulation output file.  

**Interface**
![Screenshot From 2024-11-16 23-17-31](https://github.com/user-attachments/assets/e101959f-53be-47c2-b315-377984f20ab7)

**Simulation Interface**
![Screenshot From 2024-11-16 23-17-06](https://github.com/user-attachments/assets/b53412e5-27e2-4dc6-93f2-47f6e2d6db2c)

**Simulation output**
![Screenshot From 2024-11-16 23-18-29](https://github.com/user-attachments/assets/1ce6d3f8-668d-43ad-a905-37cd17997594)

**After applying mathematical function**
![Screenshot From 2024-11-16 23-20-26](https://github.com/user-attachments/assets/1fa0d4b2-9a9a-456a-96c0-7604e1a763c7)


### News Analysis Features (Python Code)  
- Automatically fetches and analyzes news content using a free-tier API.  
- News analysis results include:  
  1. Sentiment score (1 to 5):  
     - **1**: Strongly Negative  
     - **2**: Negative  
     - **3**: Neutral  
     - **4**: Positive  
     - **5**: Strongly Positive  
  2. Reliability score (0 to 1):  
     - Example: `0.9345` (Highly Reliable), `0.2102` (Unreliable)  
  3. Summary of the news content.  
- News links are processed automatically, requiring minimal manual input.  


![Screenshot From 2024-11-16 23-42-09](https://github.com/user-attachments/assets/680ae13f-eb24-4d4b-9c35-d8022c9e7d15)

---

## Technologies Used  
- **Algorithms and Data Structures:** Core logic implemented in C.  
- **Machine Learning (ML):** Utilized Python and the `BART` model for news analysis and sentiment scoring.  
- **Mathematical Analysis:** Key functions and algorithms written in C for precise control and performance.  

---

## How to Run the Program

## Python side  
- The output of the "first tactic" function in version 1.2 is messy and requires additional cleaning, handled by a separate Python script.  
- The Python-based news analysis requires significant dependencies (gigabytes in size), making it challenging for widespread deployment in its current state.  

### C Code  
1. Ensure you have a C compiler and `make` installed.  
2. Navigate to the directory containing the source files.  
3. Execute makefile.  

