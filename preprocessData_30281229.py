# Author: Deepali Vinay (30281229)
# Start Date: 14th May 2019
# Last Modified Date: 23th May 2019


"""
Functionality: Conducting a number of pre-processing tasks to clean dataset and
               saving the contents of questions and answers as two individual output files
"""


# Function to pre-process the data of each line in the dataset, by converting character sequence, special characters and removing HTML tags
def preprocessLine(inputLine):

    import re                                   # Importing regular expressions module

    charRef =  inputLine.replace("&amp;", "&").replace('&quot;', '"')\
        .replace("&apos;", "'").replace("&gt;", ">").replace("&lt;", "<")\
        .replace("&#xA;", " ").replace("&#xD;", " ")\
        .replace("&amp;", "&").strip()          # Replacing each character reference with its original form and stripping the blank spaces at the beginning and end of the line

    return re.sub(r'<row.*?Body="|<[a-zA-Z].*?>|</[a-zA-Z].*?>|" />', '', charRef).strip()   # Returning each line after removing HTML tags and stripping blank spaces at the beginning and end of the line


# Function to generate questions file and answers file from the input file based on PostTypeId
def splitFile(inputFile, outputFile_question, outputFile_answer):


    ip = open(inputFile, errors="ignore")           # Opening the input file and ignoring UnicodeDecodeError
    opQues = open(outputFile_question, "w")         # Creating questions output file
    opAns = open(outputFile_answer, "w")            # Creating answers output file
    lines = ip.readlines()                          # Reading the whole input file and storing it as a list with each line in the input file as list element

    # Going through each line of the input file stored as individual elements in a list excluding first two lines and the last line.
    for eachLine in range(2, len(lines) - 1):

        # Writing each line in questions output file if PostTypeId is 1
        if 'PostTypeId="1"' in lines[eachLine]:
            opQues.write(preprocessLine(lines[eachLine]) + "\n")

        # Writing each line in answers output file if PostTypeId is 2
        elif 'PostTypeId="2"' in lines[eachLine]:
            opAns.write(preprocessLine(lines[eachLine]) + "\n")

    opQues.close()                                   # Closing questions output file
    opAns.close()                                    # Closing answers output file
    ip.close()                                       # Closing input file


if __name__ == "__main__":

    f_data = "data.xml"
    f_question = "question.txt"
    f_answer = "answer.txt"

    splitFile(f_data, f_question, f_answer)