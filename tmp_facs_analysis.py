#!/usr/bin/env python
# coding: utf-8

# # Load all necessary packages to run this script

# In[1]:


import pandas as pd #package to modulate dataframes (aka tables)
import seaborn as sns #advanced package for data visualization
import matplotlib.pyplot as plt #basic package for data visualization
import numpy as np #package for numeric calculations
import itertools #funny package to do combinatorics and other stuff
from statannot import add_stat_annotation #package for statistical annotation


# # Give all necessary information to run the script (read carefully the instructions!!!)

# In[2]:


#THIS IS THE ONLY PART OF THE SCRIPT YOU MUST DO SOMETHING! PLEASE GIVE ALL THE NECESSARY INFORMATION BELOW.
#YOU CAN STILL CHANGE THE INFORMATION AND RERUN THE SCRIPT.



#PART 1: FILES AND DIRECTORIES
#GIVE THE PATHS TO THE INITIAL FILES (FILE1: GATING-STRATEGY, FILE2: CELL_COUNT TABLE; BOTH IN CSV FORMAT)
GATING = r"C:\Users\pasca\Documents\Working_dir\Table_BM_Trumpp.csv"
CELL_COUNTS = r"C:\Users\pasca\Documents\Working_dir\cell_counts.csv"

#DEFINE HERE YOUR OUTPUT-DIR (THE OUTPUT FILES WILL BE SAVED HERE)
OUTPUT_DIR = r"C:\Users\pasca\Documents\Working_dir"



#PART 2: DEFINE YOUR STARTING POPULATION (WHICH POPULATION IS THE CALCULATIONS BASED ON? 
#IN MOST OF THE CASES IT WILL BE THE "coi/db" POPULATION)
#REMARK: LEAVE AWAY THE "FREQ. OF PARENT" PART AND ADD NO SPACES! EXAMPLES: "coi", "coi/db", "coi/db/lin-"
start_pop = "coi/db/lin-"



#PART 3: GRAPHICAL COSMETICS
#DEFINE THE GROUP-ORDER FOR THE GRAPHS (ATTENTION: LEAVE AWAY THE "_1.fcs" PART)
order = ["B", "S"]

#DEFINE THE NAME OF THE COMPARTMENT/ORGAN ANALYZED
organ = "BM lin-"

#IF YOU GIVE A CELL_COUNTS TABLE, AT WHICH POWER ARE THE NUMBERS GIVEN
#E.G. WHEN YOU GAVE THE NUMBERS TIMES MILLIONS (X10^6), IT IS THE POWER OF 6
power = "6"



#PART 4: NAMING OF GROUPS
#THIS CODE CONCLUDES THE GROUP NAMES FROM THE SAMPLE NAMES. AN EXAMPLE:
    #SAMPLE NAME: B_1_001.fcs
    #GROUP NAME: B
#THIS MEANS THAT IN THIS CASE, THE PART "_1_001.fcs" WILL BE REMOVED FOR THE GROUP NAME.
#I DID NOT FIND A PROPER SOLUTION TO DO THIS AUTOMATICALLY, THEREFORE YOU MUST GIVE ME THE INFORMATION
#WHICH PART OF THE SAMPLE NAME HAS TO BE REMOVED (THIS DEPENDS ON YOUR NOMENCLATURE AND THE FACS-MACHINE)
part_to_remove = "_1_001.fcs"



#PART 5: STATISTICS
#DO YOU WANT TO ADD STATISTICS? YES OR NO.
stat_ind = "yes"

#IF YOU HAVE MORE THAN 2 GROUPS, DO YOU WANT TO USE A CONTROL GROUP FOR STATISTICAL COMPARISON?
single_comp = "no"

#IF YES, PLEASE GIVE THE NAME OF THE CONTROL GROUP (ATTENTION: LEAVE AWAY THE "_1.fcs" PART):
#REMARK: IN CASE YOU HAVE ONLY TWO GROUPS, IGNORE THIS VARIABLE
control_group = "BM_all"

#CHOOSE STATISTICS TEST (AVAILABLE ARE t-test_ind, t-test_welch, 
#t-test_paired, Mann-Whitney, Mann-Whitney-gt, Mann-Whitney-ls, Levene, Wilcoxon, Kruskal)
stat_test = "t-test_welch"



#PART 6: SAVING THE GRAPHICS
#CHOOSE THE DATATYPE
datatype = "png"

#CHOOSE THE SIZE (IN DPI)
size = 300


# # Step 1: Import and modify the table received from Flojo (just run it)

# In[3]:


#Step 1: import csv file with gating strategy
BM_gating = pd.read_csv(GATING, sep=';', index_col=0)

#Step 2: Define types of all columns as string
BM_gating = BM_gating.astype(str)

#Step 3: Modify the columns itself (remove the %, change the values to numeric types, 
#divide the numbers by 100)
for column in BM_gating:
    BM_gating[column] = BM_gating[column].str.split(" ", expand=True)[0]
    BM_gating[column] = BM_gating[column].apply(pd.to_numeric)
    BM_gating[column] = BM_gating[column]/100

#Step 4: Modify the column titles (remove the "Frequency of Parent" part, remove all commas and spaces)
coi = BM_gating.columns[0]
to_keep = coi.split(" ")[0]
BM_gating = BM_gating.rename(columns = lambda x : str(x)[:-(len(coi)-len(to_keep))])
BM_gating.columns = BM_gating.columns.str.replace(' ', '')
BM_gating.columns = BM_gating.columns.str.replace(',', '')
BM_gating.columns = BM_gating.columns.str.replace(':', '_')

#Step 5: Remove the mean and SD rows, remove the first two columns 
#(correspond to the gates for the cells of interest and the doublette-free gate)
BM_gating = BM_gating.drop(["Mean", "SD"])
coi = BM_gating.columns[0]
db = BM_gating.columns[1]
BM_gating = BM_gating.drop([coi, db], axis=1)

#Step 6: Show the final dataframe
BM_gating


# # Step 2: Calculate the results in % of total cells (for each of the gated populations individually)

# In[4]:


#Step 1: Prepare the results dataframe

results = pd.DataFrame()
colname = BM_gating.columns[0]
results[start_pop] = BM_gating[colname]
results[start_pop] = 100

results


# In[6]:


#Calculate the results in percentage using a for-loop

#Step 2: Create a string (test) and an empty list for further manipulation
substring = start_pop
stringlist = []
count = 0

#Step 3: Iterate through the Percentage-Table (column by column)
for column in BM_gating:
    
    if substring in column: #check if my set substring is contained in the column name
        if column == start_pop:
            stringlist.append(column)   
        else:
            results[column] = results[substring] * BM_gating[column] #if substring is part of column name, do the calculations
            substring = str(column) #reset the variable "substring" with the column name
            stringlist.append(column) #add the column name as an element to the stringlist
            #print(stringlist)
            #count = count+1
            #print(count)

    else: #if my column name is not contained in the previous column, the code continues here
        working_list = [] #create another empty list
        for element in stringlist: #iterate over the stringlist (contains the names of all previous columns)
            if element in column: #if one of the previous columns is contained in the current column, the name will be added to the working_list
                working_list.append(element)
        max_value = max(working_list, key=len) #create the variable "max_value", which contains the longest element form the working_list
        results[column] = results[max_value] * BM_gating[column] #use the max_value column name to calculate the value of the new column
        substring = str(column)
        stringlist.append(column)
        #print(stringlist)
        #count = count+1
        #print(count)

filepath = OUTPUT_DIR + "\\results_percentage.csv"
results.to_csv(filepath)

results


# # Step 3: Visualize the percentages of total cell population

# # Attetion with Pre-Step 1! I still didn't find a proper solution here, double-check the result of the "group" column if the group names are correct!

# In[7]:


#Pre-Step 1: Add a group column to the results dataframe
results['group'] = results.index
results["group"] = results["group"].str[:-len(part_to_remove)]
results = results.drop(db, axis=1, errors='ignore')

results


# In[9]:


#Pre-Step 2: Get the necessary group information for the statistical analysis
pairs = results["group"].tolist()
pairs = list(set(pairs))
n_pairs = len(pairs)
tuple_comp = []

if stat_ind == "yes": 
    if n_pairs <= 2:
        tuple_comp = [tuple(pairs)]
    elif single_comp == "yes":
        for pair in itertools.combinations(pairs,2):
            tuple_comp.append(pair)
        tuple_comp = [item for item in tuples if control_group in item]
    else:
        for pair in itertools.combinations(pairs,2):
            tuple_comp.append(pair)

print(tuple_comp)


# In[10]:


#Step 1: Set necessary settings for Seaborn
split = "/"
sns.set_style("ticks")
sns.set_palette("Dark2")

#Step 2: Visualize the data column by column using a for-loop
for column in results:
    if column != str("group"):
        ax = sns.catplot(kind="bar", 
                         data=results, 
                         y=column, 
                         x="group", 
                         ci="sd", 
                         edgecolor="black", 
                         errcolor="black", 
                         errwidth=1.5, 
                         capsize = 0.1, 
                         alpha=0.3, 
                         order = order)
        ax = sns.stripplot(x="group", 
                           y=column, 
                           data=results, 
                           dodge=True, 
                           alpha=1,
                           linewidth=3, 
                           order = order)
        plt.xlabel(None)
        plt.ylabel((column.split(split)[-1] + " (%of total " + organ + ")"), fontsize = 17)
        plt.title(column.split(split)[-1], fontsize=20)
        plt.xticks(rotation=45)
        plt.tick_params(axis='both', which='major', labelsize=14)
        
        if stat_ind == "yes":   
            add_stat_annotation(ax, 
                                data=results, 
                                x="group", 
                                y=column, 
                                order=order,
                                box_pairs=tuple_comp,
                                test=stat_test, 
                                text_format='star', 
                                loc='inside', 
                                verbose=2, fontsize=15)
        
        plt.savefig(OUTPUT_DIR + "\\" + column.split(split)[-1] + "_percentage_of_tot" + "." + datatype, dpi=size, bbox_inches="tight")


# # Step 4: Calculate the absolute counts

# In[68]:


#Step 1: Import csv file with cell counts and modify it
count_table = pd.read_csv(CELL_COUNTS, sep=';', index_col=0)
count_table = count_table.rename(columns={count_table.columns[0]: start_pop})
count_table = results.merge(count_table, suffixes=("_results", "_count"), left_index=True, right_index=True)
count_table = count_table[["coi/db/lin-_count"]]
count_table = count_table.rename(columns = lambda x : str(x)[:-6])

count_table


# In[69]:


#Calculate the absolute cell counts using a for-loop

#Step 2: Create a string (test) and an empty list for further manipulation
substring = start_pop
stringlist = []
count = 0

#Step 3: Iterate through the Percentage-Table (column by column)
for column in BM_gating:
    
    if substring in column: #check if my set substring is contained in the column name
        if column == start_pop:
            stringlist.append(column)   
        else:
            count_table[column] = count_table[substring] * BM_gating[column] #if substring is part of column name, do the calculations
            substring = str(column) #reset the variable "substring" with the column name
            stringlist.append(column) #add the column name as an element to the stringlist
            #print(stringlist)
            #count = count+1
            #print(count)

    else: #if my column name is not contained in the previous column, the code continues here
        working_list = [] #create another empty list
        for element in stringlist: #iterate over the stringlist (contains the names of all previous columns)
            if element in column: #if one of the previous columns is contained in the current column, the name will be added to the working_list
                working_list.append(element)
        max_value = max(working_list, key=len) #create the variable "max_value", which contains the longest element form the working_list
        count_table[column] = count_table[max_value] * BM_gating[column] #use the max_value column name to calculate the value of the new column
        substring = str(column)
        stringlist.append(column)
        #print(stringlist)
        #count = count+1
        #print(count)

filepath = OUTPUT_DIR + "\\results_absolute.csv"
count_table.to_csv(filepath)

count_table


# # Step 5: Visualize the absolute counts

# # Attetion with Pre-Step 1! I still didn't find a proper solution here, double-check the result of the "group" column if the group names are correct!

# In[70]:


#Pre-Step 1: Add a group column to the count_table dataframe
count_table['group'] = count_table.index
count_table["group"] = count_table["group"].str[:-len(part_to_remove)]
count_table = count_table.drop(db, axis=1, errors='ignore')

count_table


# In[83]:


#Pre-Step 2: Set necessary settings for Seaborn
split = "/"
sns.set_style("ticks")
sns.set_palette("Dark2")

#Step 3: Visualize the data column by column using a for-loop
for column in count_table:
    if column != str("group"):
        ax = sns.catplot(kind="bar", 
                         data=count_table, 
                         y=column, 
                         x="group", 
                         ci="sd", 
                         edgecolor="black", 
                         errcolor="black", 
                         errwidth=1.5, 
                         capsize = 0.1, 
                         alpha=0.3, 
                         order = order)
        ax = sns.stripplot(x="group", 
                           y=column, 
                           data=count_table, 
                           dodge=True, 
                           alpha=1,
                           linewidth=3, 
                           order = order)
        plt.xlabel(None)
        plt.ylabel((organ + " " + column.split(split)[-1] + " count [x10^" + power + "]" ), fontsize = 17)
        plt.title(column.split(split)[-1], fontsize=20)
        plt.xticks(rotation=45)
        plt.tick_params(axis='both', which='major', labelsize=14)
        
        if stat_ind == "yes":   
            add_stat_annotation(ax, 
                                data=count_table, 
                                x="group", 
                                y=column, 
                                order=order,
                                box_pairs=tuple_comp,
                                test=stat_test, 
                                text_format='star', 
                                loc='inside', 
                                verbose=2, fontsize=15)
        
        plt.savefig(OUTPUT_DIR + "\\" + column.split(split)[-1] + "_absolute" + "." + datatype, dpi=size, bbox_inches="tight")


# In[ ]:




