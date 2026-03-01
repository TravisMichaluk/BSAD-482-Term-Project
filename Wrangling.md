Jobs Created by Tourism Data Cleaning: 

Data Cleaning Process

The main issue with my initial dataset was that it was formatted "wide," meaning every year and quarter had its own separate column. While that’s easy to read in a spreadsheet, Tableau couldn't recognize it as a continuous timeline, which made it impossible to build a proper trend chart.

To fix this, I had to "pivot" the data to get it into a "long" format. I consolidated all those individual date columns into one single column for the time period and another for the number of jobs created. Now that the data is structured correctly, I can actually use the date as a dimension to show how tourism employment is trending across different industries.


