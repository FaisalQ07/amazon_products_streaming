
# Stream Processing of Amazon Products Information to Identify Trends and Patterns 

# Introduction & Goals
- The objective of this project is to build a data processing pipeline that could utillize the modern tech stack for data engineering.  
  The teck stack is the classic data engineering platform blueprint comprising of:
    * API connecting to the data source.
    * Buffer, to persist the data temporarily until they are ready to be processed
    * Processing framework, a distributed system for parallel data processing and fault tolerance
    * Storage, to store the processed data
    * Vizualization, tools to create interactive reports where stakeholders can explore data, drill down into details, and gain insights by interacting with the visualizations
  

- To achieve the objective, Amazon dataset is taken from the open source platform Kaggle. The dataset comprises of two files, amazon categories and products.
  Together, these files provide information regarding the sales, ratings, prices of the products based on their categories.
  The goal of using this dataset is to:
    * Analyse the distribution of price levels for products sold
    * Analyse the distribution of categories for products sold
    * Analyse the average price for each category

 - In order to process that data and provide the reports for analysis, following tools are used:
   * [API-Ingest](#connect)
   * [Kafka](#buffer)
   * [Spark](#processing)
   * [Mongodb](#storage)
   * [Streamlit](#visualization) 
  
- Write this like an executive summary
  - With what data are you working
  - What tools are you using
  - What are you doing with these tools
  - Once you are finished add the conclusion here as well

# Contents

- [The Data Set](#the-data-set)
- [Used Tools](#used-tools)
  - [Connect](#connect)
  - [Buffer](#buffer)
  - [Processing](#processing)
  - [Storage](#storage)
  - [Visualization](#visualization)
- [Pipelines](#pipelines)
  - [Stream Processing](#stream-processing)
    - [Storing Data Stream](#storing-data-stream)
    - [Processing Data Stream](#processing-data-stream)
  - [Batch Processing](#batch-processing)
  - [Visualizations](#visualizations)
- [Demo](#demo)
- [Conclusion](#conclusion)
- [Follow Me On](#follow-me-on)
- [Appendix](#appendix)


# The Data Set
- Explain the data set
- Why did you choose it?
- What do you like about it?
- What is problematic?
- What do you want to do with it?

# Used Tools
- Explain which tools do you use and why
- How do they work (don't go too deep into details, but add links)
- Why did you choose them
- How did you set them up

## Connect
## Buffer
## Processing
## Storage
## Visualization

# Pipelines
- Explain the pipelines for processing that you are building
- Go through your development and add your source code

## Stream Processing
### Storing Data Stream
### Processing Data Stream
## Batch Processing
## Visualizations

# Demo
- You could add a demo video here
- Or link to your presentation video of the project

# Conclusion
Write a comprehensive conclusion.
- How did this project turn out
- What major things have you learned
- What were the biggest challenges

# Follow Me On
Add the link to your LinkedIn Profile

# Appendix

[Markdown Cheat Sheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
