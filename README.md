
# Association Rules Extraction (COMS 6111 - Fall 17 - Project 3)

Implementation of an association rules extractor using the « A priori algorithm » and used to analyze a dataset of NYPD complaints for the year of 2016. The main part of the algorithm relies on an enhanced version of the commonly known « A priori algorithm » described by Agrawal and Srikant in the paper « Fast Algorithms for Mining Association Rules » in VLDB 1994. The dataset in this repository is an already transformed version of a dataset that can be found on NYC Open Data, where columns have been dropped and transformed using Python (Pandas) for the needs of our analysis and saved into a CSV file.

This is a project that I developped in Fall 2017 for the course COMS 6111 Advanced Database Systems taught by Professor Luis Gravano at Columbia University.
Below are the instructions and the readme that I submitted for the project.

## Submitted files

* README.md
* association_rules_extractor
    * __main__.py
    * a_priori.py.py
    * helpers.py
    * select_confidence.py
* data
    * INTEGRATED-DATASET.csv
* example-run.txt

## How to install & run

### Install

The program itself (i.e. not including the dataset generation) relies only on built-in Python (3.6) libraries and types, therefore no preliminary step is needed to install the program and no package needs to be installed to run it.

### Run
From the top level folder, run the project with:
```
python3 -m association_rules_extractor <filename> <min_sup> <min_conf>
```
For example:
```
python3 -m association_rules_extractor data/INTEGRATED-DATASET.csv 0.05 0.3
```

## Dataset

### a. The dataset used

The dataset that I used is the NYPD Complaint Map available at "https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Map-Year-to-Date-/2fra-mtpn" which contains information about all the complaints received by the NYPD for the year of 2016 with information on time, location and the type of complaint. The idea for this choice was to identify associations between parts of the city, periods of the day and types of crime (which range from small fellonies to serious crimes).

### b. The procedure used to map the original dataset into the INTEGRATED-DATASET file

- I first selected a few interesting attributes among the attributes contained in the original dataset (more than 20), namely attributes referring to date/time, description of the offense, and location: Therefore I dropped all columns except *'CMPLNT_FR_DT', 'CMPLNT_FR_TM','OFNS_DESC', 'BORO_NM', 'ADDR_PCT_CD', and 'LOC_OF_OCCUR_DESC'.*

- I modified these attributes to find the proper level of granularity and a correct distribution to find interesting rules. I'll explain these choices in the next part. Here are the transformation I did over the attributes:
    - **Date**: 'CMPLNT_FR_DT' was transformed to keep the day of the week (as a string)
    - **Time**: 'CMPLNT_FR_TM' was transformed and the time in the day was divided into 4 periods: 'MORNING' (6 am to 11:59 am), 'AFTERNOON' (12 pm to 4:59 pm), 'EVENING' (5 pm to 9:59 pm) and 'NIGHT'.
    - **Offense**: 'OFNS_DESC' was let untransformed. We might use the corresponding offense code (included in the dataset) to speed the procedure at a larger scale and save memory (use ints instead of string), yet keeping this attribute as a strings lets us have readable association rules without post processing
    - **Location**: The borrough ('BORO_NM') was kept, and 'ADDR_PCT_CD' which contains the Precinct number (which is a more granular grid of NY) was dropped. 'LOC_OF_OCCUR_DESC' was also dropped, which is the attribute that roughly describes if the event happened inside or outisde.
    
- These transformation were performed using Pandas (in particular the method DataFrame.apply with custom functions)

### c. What makes the choice of the dataset compelling

- In terms of application, the dataset lets us understand how crimes are distributed among the boroughs. As a first approximation, one could guess that some boroughs such as Bronx are predominant among crimes in NYC. This dataset lets us have a deeper look at crimes, especially thanks to offense description: We'll see that depending on the nature of offenses, some boroughs are more represented than others. We'll also learn how offenses are related to the time of the day / the day of the week.
- This dataset contains more than 350,000 rows, which will be useful to derive significant rules. NYC Open Data also contains a dataset with similar data for other years than 2016: 5,5 million rows for offenses from 2006 to 2016. One intereseting further analysis would be to derive association rules for each year and observe how they evolved over a decade.
- The challenge over this dataset was to find the proper level of granularity for each dimension to learn both interesting and accurate relations:
    - **Date**: The original dataset contains the full date for each day of 2016. Of course, some aggregation was needed, so that the resulting transactions contain duplicates which can be grouped and therefore lead to association rules. My first attempt was to reduce dates to months, yet there didn't seem to be an interesting correlation between the month and the offenses. I therefore decided to choose a further granularity and use days of the week, the intuition being that there will probably be more crimes during weekends.
    - **Time**: The originald dataset contains times as HH:MM:SS. Reducing to hours is too granular. My first attempt was to divide a day between morning (before noon), and afternoon. This lead to most association rules involving 'afternoon' in the right hand side, the reason being that the dataset mostly contains offenses in the afternoon. In particular, each borrough lead to a relation to 'afternoon', which is not relevant at all. The final split of the day in 4 periods lead to roughly balanced splits (18,7 % / 27,3 % / 27,7 % / 26,2 %). The 'morning' category is still less represented, yet it truly represents the distribution of offenses and extending the range of morning to have more balanced classes would introduce bias in the analysis.
    - **Offense**: The offense description from the dataset provides a good level of granularity. The dataset contains also a less granular 'level of offense' (felony, misdemeanor, violation), yet this leads to less interesting rules and we have enough data to use the first, more granular, attribute.
    - **Location**: For reasons similar to the other dimensions, I chose borough and dropped precincts or lat/long, which both also represent location. With more data, it would be interesting to analyse precinct, yet over this dataset using precinct didn't lead to interesting rules. Obviously, lat/long, even if grouped by ranges, is too granular.

## e) Internal design



The internal design of the program is straightforward:

- **__main__.py**: contains the main logic of the program, i.e:
    - loading and parsing the csv
    - running the a priori algorithm to extract large itemsets (itemsets above minimum support)
    - select high confidence rules

- **a_priori.py**: contains the implementation of the a priori algorithm in a_priori(). Note that this method takes as input the function to generate candidates of size k+1 given the list of large itemsets of size k. This modularity lets us use different implementations for this part which has the most impact on efficiency in the procedure.
    - By default, a_priori() uses the method generate_candidates_enhanced() which corresponds to the implementation described in Section 2.1 of the Agrawal and Srikant paper in VLDB 1994.
    - The procedure also contains a method generate_candidates() (which is not used by default), which is a naive implementation for this step. See part g) for a comparison of both methods.

- **helpers.py**: contains methods that are not important for the main logic, namely methods either to load the csv or print different steps of the procedure. It also contains the methods used to generate the dataset (which are not called in the procedure but were left in the code), which are all commented out to avoid having to add pandas to the requirements.

- **select_confidence.py**: takes the list of large itemsets and the already computed supports, both outputs of the a priori algorithm, generates a list of tuples (LHS,RHS) which contain partitions of each large itemset of size > 1 with RHS of size exactly 1, and returns tuples which have sufficient confidence. Note that the confidence is computed with the formula: confidence((LHS,RHS)) = support(LHS U RHS)/support(LHS) which can be derived easily from the definitions of confidence and support.

## f) Command line specification



An interesting sample run is with **min_sup = 5 % and min_conf = 20 %.**

- This run leads to 28 association rules.


- The highest support is 8.2 % achieved by:
    - **(1)** 'EVENING'  =>  'BROOKLYN' (conf. 29.57 %, sup. 8.2 %) and its opposite ('BROOKLYN' => 'EVENING', conf. 27.84 %).
    - Compared to a uniform distribution on the 5 boroughs (20%), this means that offenses in the evening are significantly more often in Brooklyn than in other boroughs.
    
- The highest confidence is 34.02 %, achieved by:
    - **(2)** 'PETIT LARCENY' => 'AFTERNOON' (conf 34.02 %, sup. 6.02 %).
    - This rule is very interesting and tells us that (compared to a uniform distribution on the 4 periods of the day, 25 %), when there is an offense of type petit larceny, most of the time it happens in the afternoon.


- Except (1), other rules of type **'PERIOD OF DAY' => 'BOROUGH'** are numerous, therefore not always interesting when confidence is too small. Among them here are the ones that seem relevant and interesting:
    - **(3)** 'NIGHT' => 'BROOKLYN' (conf. 30 %, sup. 7.87 %). As for relation (1), the confidence is large enough to infer interestingness and relevancy. Other relations 'NIGHT' => 'BOROUGH' are all similar in terms of confidence and support.
    - **(4)** 'MORNING' => 'BROOKLYN'(conf. 29.84 %, sup. 5.58 %). This is the only relation of type 'NIGHT' => 'BOROUGH' above threshold, probably because there are less offenses in the morning and therefore candidates do not pass the support threshold.
   - **(5)** 'AFTERNOON' => 'BROOKLYN' (conf 28.51 %, sup. 7.8 %) is once again predominant, yet it is interesting to note that **(6)** 'AFTERNOON' => 'MANHATTAN' is close (conf. 26.37 %, sup. 7.21 %) which was not the case for any other period of the day and borough !
   - **(7)** 'EVENING' => 'MANHATTAN' is also 2nd in confidence after (1), but with less confidence than 'AFTERNOON' => 'MANHATTAN'.
   - To conclude, for most periods of time, Brooklyn is always predominant. Yet, in the Afternoon and Evening, Manhattan is close, which is not the case for other periods where boroughs are equally represented.


- Except (2), other rules of type **'OFFENSE TYPE' => 'PERIOD OF DAY'** are rare and only include:
    - **(8)** 'PETIT LARCENY' => 'EVENING' (conf. 29.51 %, sup. 5.22 %).
    - This tells us that other types of offenses are equally spread during the day, which is a bit counter-intuitive as we would for example think that serious offenses such as 'SEX CRIME' would be much more distributed at night. Such a relation is probably absent because the support is too small, as 
    - Also, this result about petit larceny is very intuitive as during the afternoon and in the evening, streets are more crowded.
    

- Other interesting rules of other types include:
    - **(9)** 'PETIT LARCENY' => 'MANHATTAN' (conf. 30.7 %, sup. 5.43 %). Even though Brooklyn seemed to be predominant in criminal activity, petit larcenies happen more often in Manhattan.

    


## Additional section: Comments and short efficiency analysis

### Comments:

#### Limits of the metrics used

This analysis shows us that support and confidence are very basic metrics. For example, we saw that Brooklyn appears in most of the extracted rules as in general there are more offenses in Brooklyn anyway. 

Also, the program doesn't extract many rules that include the type of offense. This is because, in order not to extract too many rules, we need to set a higher minimum support. Types of offense didn't pass the threshold on minimum support, but would still be interesting. This leads us to think that using another metric to evaluate interestingness would be relevant.

Another point is that by setting a support high enough not to output too many rules, we excluded rules LHS => RHS where LHS is of size more than 1.

Yet, we could derive interesting results from this analysis, and using support and confidence allows us to use the a priori algorithm which performs quite fast on this large dataset.

#### Importance of granularity

The point on types of offense also show us the importance of granularity. We could group some types of offenses to infer more rules involving this attribute. During this project, I observed the difficulty of finding a proper trade off between fine granularity (to draw interesting conclusions) and enough aggregation to be able to actually extract rules.

We saw that no interesting rule included the day of the week. We might want to replace it with a binary attribute weekend/non-weekend, which will draw lead to more interesting rules.

### Efficiency:

Recall that our dataset has 351,509 rows, which is already high enough to observe efficiency differences. As said earlier, an interesting analysis would be over the same dataset but for a decade instead of a year, which will have 10 times more rows. In such a setting, efficiency considerations would be even more important.

#### Naive implementation of candidates choice:

For the sample run described in part f), a naive implementation of the choice of candidates (large itemsets) in the a priori algorithm leads to:

- Itemsets of size 1: 76 candidates
- Itemsets of size 2:1310 candidates
- Itemsets of size 3: 1139 candidates

- Total running time: 96 sec

#### Enhanced implementation of candidates choice:

For the sample run described in part f), with the default enhanced algorithm for generating large itemsets candidates (as described in the readings), we have: 

- Itemsets of size 1: 76 candidates
- Itemsets of size 2: 190 candidates
- Itemsets of size 3: 47 candidates

- Total running time: 15 sec

#### Comparison

We can observe that there is a factor 10 between the number of candidates considered in the two algorithms, which is a significant difference. This reflects in the running times which is 6 times faster for the enhanced implementation.

Of course, this is a very simple comparision and we would need more performance tests to do a proper performance analysis.

#### About data structures

In this project, for the sake of simplicity, we used basic data structures provided by python. In particular, all the data is in memory, which would probably not be feasible with a larger dataset. One solution that I would consider to scale this program would be to use SQLite which would allow to easily store data on disk and perform the operations needed.
