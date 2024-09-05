# NREL_DataMining
A Practice/Showcase project of NREL Dataset mining

Premise: 
The NSRDB is a database collection of meteorological data containing measurements calculating solar radiation which can be converted to energy. NSRDB is a publicly available database which charges nothing for their data.

Goal:
Set up options for Data Mining Analysis techniques to be done on data from a specific region if available. 

Goal includes:
- Set up ETL Process to make data readable to the machine using python
- Data Mining Methods using C
- Add Filter Options to the search

Unit Testing:

For unit testing framework focused around the data mining methods, Unity was chosen due to its portability and ease of use. 

Link to Unity Website: https://www.throwtheswitch.org/unity

Unity's files were not included in this repository due to the amount of files, the use of unity and its files can be seen in the test file headers and Makefile configuration. 

To call for unit testing, this line was used 'make test'

That line results in a new directory called build which holds the results of the tests ran as well as the necessary components needed to make unity work. 
