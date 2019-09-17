# Author: Deepali Vinay (30281229)
# Start Date: 20th May 2019
# Last Modified Date: 24th May 2019

"""
Functionality: This program generates 2 graphs, a bar graph showing the number of posts spread across different
			   vocabulary sizes and another line graph showing the number of post(different type:Question/Answer)
			   spread across quarters of subsequent years.
"""

import numpy as np                              # Importing numpy module as np
import pandas as pd                             # Importing pandas module as pd
import matplotlib.pyplot as plt                 # Importing pyplot from matplotlib module as plt
from parser_30281229 import Parser              # Importing class Parser from another python program parser_30281229 in current working directory


def visualizeWordDistribution(inputFile, outputImage):
    # Function that reads the inputfile and saves the plot as specified file name in the argument

    f = open(inputFile, errors="ignore")            # Open specified file, ignoring the decoding errors
    lines = f.readlines()[2:]                       # Reading all lines except the first two and storing them in a list
    s = pd.Series()                                 # Creating an empty series which will hold the VocabularySize with ID as index

    # Iterating over whole lines list except the last element
    for i in range(len(lines) - 1):
        parsed = Parser(lines[i])                   # Instantiating the class Parser with the ith element of list lines
        s = s.append(pd.Series([parsed.vocabularySize],\
                        index=[parsed.ID]))         # appending VocabularySize of ith element of lines with ID as index to series s
    bins = pd.cut(s, np.append(np.arange(0, 110, 10), np.inf),\
                  labels=('0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100', 'Others'),
                  right=False)                      # Replacing each value in the series s with the corresponding left inclusive ranges
    binCount = bins.value_counts(sort=False)        # Counting occurances of each bin
    ax = binCount.plot(kind='bar', color='mediumvioletred',\
                       figsize=(10, 6),rot=70)      # Plotting the bar chart for bins v/s binCount
    ax.set_xlabel("Vocabulary Count", labelpad=20, weight='bold', size=12)  # Setting the label for x-axis
    ax.set_ylabel("Number of Posts", labelpad=20, weight='bold', size=12)   # Setting the label for y-axis
    ax.set_title("Word Distribution", weight='bold', size=15)               # Setting the title of the graph
    ax.grid()                                       # Turning on grids
    plt.savefig(outputImage,bbox_inches="tight")    # Saving the chart to the file name specified in argument when the function is called


def visualizePostNumberTrend(inputFile, outputImage):
    # Function that reads the inputfile and saves the plot as specified file name in the argument
    f = open(inputFile, errors="ignore")            # Open specified file, ignoring the decoding errors
    lines = f.readlines()[2:]                       # Reading all lines except the first two and storing them in a list
    id = []                                         # Initializing empty list for ID
    quart = []                                      # Initializing empty list for quarter
    typ = []                                        # Initializing empty list for type

    # Iterating over whole lines list except the last element
    for i in range(len(lines) - 1):
        parsed = Parser(lines[i])                   # Instantiating the class Parser with the ith element of list lines
        id.append(parsed.ID)                        # Appending extracted ID from parsed object to list id
        quart.append(parsed.dateQuarter)            # Appending extracted dateQuarter from parsed object to list quart
        typ.append(parsed.type)                     # Appending extracted type from parsed object to list typ

    df = pd.DataFrame({'ID': id, 'Quarter': quart, 'Type': typ}) # Creating a DataFrame using dictionary format, which is created from the 3 lists id, quart and typ
    dfq = df[df.Type == 'Question']                 # Creating another DataFrame by filtering only Question type from 'df'
    dfa = df[df.Type == 'Answer']                   # Creating another DataFrame by filtering only Answer type from 'df'
    grouped_questions = dfq.groupby('Quarter').size().reset_index(name='Question')  # Grouping dfq by Quarter, and taking the count of each quarter
    grouped_answers = dfa.groupby('Quarter').size().reset_index(name='Answer')      # Grouping dfa by Quarter, and taking the count of each answer
    ax = grouped_answers.plot(kind='line', x='Quarter', y='Answer', marker='o',color='mediumspringgreen',
                              xticks = range(len(grouped_questions['Quarter'])))    # Plotting the line chart for Quarter v/s Answers(Count)
    grouped_questions.plot(kind='line', ax=ax, y='Question', marker='^', figsize=(10, 4),
                           color='darksalmon',rot = 70)                             # Plotting the line chart for Quarter v/s Question(Count) in same axis ax
    ax.set_xlabel("Quarter", labelpad=20, weight='bold', size=12)                   # Setting the label for x-axis
    ax.set_ylabel("Number of Posts", labelpad=20, weight='bold', size=12)           # Setting the label for y-axis
    ax.set_title("PostNumberTrend", weight='bold', size=15)                         # Setting the title of the graph
    ax.legend()                                                                     # Turning on Legend
    ax.grid()                                                                       # Turning on Grids
    plt.savefig(outputImage, bbox_inches="tight")                                   # Saving the chart to the file name specified in argument when the function is called


if __name__ == "__main__":
    f_data = "data.xml"
    f_wordDistribution = "wordNumberDistribution.png"
    f_postTrend = "postNumberTrend.png"

    visualizeWordDistribution(f_data, f_wordDistribution)
    visualizePostNumberTrend(f_data, f_postTrend)