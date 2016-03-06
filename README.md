# Abstraction
Insight data science project 2016.

This repository contains my Insight data science project from the January/Feburary 2016 session called Abstraction.  It's a text based recommendation app for scientific literature.  Given a description of your research interests, the app finds the most likely interesting scientific articles for you based on a database of approx 50000 articles worth of metadata.  All of the metadata comes from Arxiv.org.  Currently, the database best spans theoretical high energy physics, but also touches the cross listed subjects like math, CS, astrophysics etc.  In this repository you'll find the code which accesses the Arxiv API and gets the metadata, a few preprocessing programs for the text data, a TF-IDF classification, LDA topic modeling and a few examples of time series analysis with ARIMA models.  There is also a web-app contained in here as well, which is running on abstraction.me.  

The program GetDataRestart.py calls the Arxiv API and gets the metadata for the articles.  The search parameters and the number of queries to make can be adjusted as well as the wait time between queries.  
