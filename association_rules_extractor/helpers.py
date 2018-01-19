import csv

# --------------------- Functions used in main() --------------------- #

def load_csv(filename):
    """Loads a csv of transactions and returns a list of transactions represented as sets"""
    transactions = []
    with open('data/INTEGRATED-DATASET.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for transaction in reader:
            transactions.append(set(transaction))
    return transactions

def print_large_itemsets(large_itemsets, supports):
    print('=========== LARGE ITEMSETS ============\n')
    sorted_itemsets = sorted(large_itemsets, key=lambda c: supports[c], reverse=True)
    for c in sorted_itemsets:
        print('{ %s },  support: %s' % (', '.join(list(c)), str(round(100*supports[c], 2))) + ' %')
    print('=========== END OF LARGE ITEMSETS =========\n\n')

def print_rules(selected_rules):
    """format: list of (lhs, rhs, confidence, support)"""
    print('=========== SELECTED RULES ============\n')
    sorted_rules = sorted(selected_rules, key=lambda rule: rule[2], reverse=True) # sort by confidence
    for rule in sorted_rules:
        print('')
        print(rule[0], ' => ', rule[1])
        print('confidence: ' + str(round(100*rule[2], 2)) + ' %')
        print('support: ' + str(round(100*rule[3], 2)) + ' %')
    print('=========== END OF SELECTED RULES ============\n')

def save_large_itemsets(large_itemsets, supports):
    print('Saving large itemsets to output file...')
    with open('output.txt', 'w', newline='') as file:
        sorted_itemsets = sorted(large_itemsets, key=lambda c: supports[c], reverse=True)
        for c in sorted_itemsets:
            file.write(str(list(c)) + ', ' + str(round(100*supports[c], 2)) + ' % \n')

def save_rules(selected_rules):
    print('Saving large itemsets to output file...')
    with open('output.txt', 'a', newline='') as file:
        sorted_rules = sorted(selected_rules, key=lambda rule: rule[2], reverse=True) # sort by confidence
        for rule in sorted_rules:
            file.write('\n')
            file.write(str(list(rule[0])))
            file.write(' => ')
            file.write(str(list(rule[1])))
            file.write('   (Conf: ' + str(round(100*rule[2], 2)) + ' %, ')
            file.write('Supp: ' + str(round(100*rule[3], 2)) + ' %)')

# Output the frequent itemsets and the high-confidence association rules to a file named "output.txt": 
# in the first part of this file, for the frequent itemsets, each line should include one itemset, 
# within square brackets, and its support, separated by a comma (e.g., [item1,item2,item3,item4], 7.4626%). 
# The lines in the file should be listed in decreasing order of their support. 


# In the second part of the same output.txt file, for the high- confidence association rules, 
# each line should include one association rule, with its support and confidence 
# (e.g., [item1,item3,item4] => [item2] (Conf: 100%, Supp: 7.4626%)). 

# The lines in the file should be listed in decreasing order of their confidence.

# --------------------- Functions used for dataset generation --------------------- #

# To use, uncomment, and pip install pandas

# import pandas as pd
# import datetime, math

# def period_of_day(str_time):
#     """given a time passed as string, returns if time is morning, afternoon or night"""
#     time = datetime.datetime.strptime(str_time, '%H:%M:%S').time()
#     # return time < datetime.time(12,0)
#     if time > datetime.time(6,0) and time < datetime.time(12,0):
#         return 'MORNING'
#     elif time >= datetime.time(12,0) and time < datetime.time(17,0):
#         return 'AFTERNOON'
#     elif time >= datetime.time(17,0) and time < datetime.time(22,0):
#         return 'EVENING'
#     else:
#         return 'NIGHT'

# def month(str_date):
#     """given a time passed as string, returns the month (as string)"""
#     date = datetime.datetime.strptime(str_date, '%m/%d/%Y').date()
#     return str(date.month)

# def day(str_date):
#     """given a time passed as string, returns the day of the week (as a string)"""
#     days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
#     day_nb = datetime.datetime.strptime(str_date, '%m/%d/%Y').weekday()
#     return days[day_nb]

# def generate_complaints_dataset():
#     transactions = list() # list of sets
    
#     # Prepare dataframe:
#     df = pd.read_csv('data/NYPD_Complaint_Map__Year_to_Date_.csv')
#     df = df[['CMPLNT_FR_DT', 'CMPLNT_FR_TM','OFNS_DESC', 'BORO_NM', 'ADDR_PCT_CD', 'LOC_OF_OCCUR_DESC']]
#     # df['PRECINCT'] = df['ADDR_PCT_CD'].apply(lambda x: 'PRECINCT_' + str(int(x)) if not math.isnan(x) else 'PRECINCT_UNKNOWN')
#     # df['TIME_PERIOD'] = df['CMPLNT_FR_TM'].apply(lambda x: 'morning' if is_morning(x) else 'afternoon' )
#     df['TIME_PERIOD'] = df['CMPLNT_FR_TM'].apply(period_of_day)
#     # df['MONTH'] = df['CMPLNT_FR_DT'].apply(month) 
#     df['DAY'] = df['CMPLNT_FR_DT'].apply(day)
#     # df['LOCATION'] = df['LOC_OF_OCCUR_DESC'].apply(lambda x: 'inside' if x == 'INSIDE' else 'outside' if isinstance(x, str) else 'location_unknown')
#     df.drop(['ADDR_PCT_CD', 'CMPLNT_FR_DT', 'CMPLNT_FR_TM', 'LOC_OF_OCCUR_DESC'], axis=1, inplace=True)
    
#     # Convert to transactions:
#     transactions = list() # list of sets
#     for row in df.iterrows():
#         transactions.append(set(row[1].tolist()))
#     return transactions

# def write_csv(transactions):
#     """Given a list of transactions, writes them in a csv file"""
#     with open('data/INTEGRATED-DATASET.csv', 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile, delimiter=',')
#         for transaction in transactions:
#             writer.writerow(transaction)

# write_csv(generate_complaints_dataset())