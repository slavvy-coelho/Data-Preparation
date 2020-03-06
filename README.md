# DATA PREPARATION
## Aim: <br>
Data scientists often spend 80% of their time on data preparation. If your career goal is to become a data scientist, you have to master data cleaning and data integration skills. In this assignment, you will learn how to solve the Entity Resolution (ER) problem, a very common problem in data cleaning and integration. After completing this assignment, you should be able to answer the following questions: <br>
<ol> 
<li>What is ER?</li>
 <li>What are the applications of ER in data integration and cleaning?</li>
 <li>How to avoid $n^2$ comparisons?</li>
 <li>How to compute Jaccard Similarity?</li>
 <li>How to evaluate an ER result?</li> </ol><br>

### Overview<br>
ER is defined as finding different records that refer to the same real-world entity, e.g., iPhone 4-th generation vs. iPhone four. It is central to data integration and cleaning. In this assignment, you will learn how to apply ER in a data integration setting. But the program that you are going to write can be easily extended to a data-cleaning setting, being used to detect duplication values.

Imagine that you want to help your company's customers to buy products at a cheaper price. In order to do so, you first write a web scraper to crawl product data from Amazon.com and Google Shopping, respectively, and then integrate the data together. Since the same product may have different representations in the two websites, you are facing an ER problem.

Existing ER techniques can be broadly divided into two categories: 
<ol><li>similarity-based (Part 1) 
<li>learning-based (Part 2).</ol><br>

### Part 1: Similarity Based<br>
<UL> 
<LI>Task A. Data Preprocessing (Record --> Token Set)
 <li>Task B. Filtering Obviously Non-matching Pairs
  <li>Task C. Computing Jaccard Similarity for Survived Pairs
 <li>Step D. Evaluating an ER result </ul>

### Part 2: Similarity Based<br>
<UL> 
<LI>Step 1. Read Data
 <li>Step 2. Similar Pairs
  <li>Step 3. Active Learning
 <li>Step 4. Model Evaluation </ul>
