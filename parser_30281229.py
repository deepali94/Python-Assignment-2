# Author: Deepali Vinay (30281229)
# Start Date: 17th May 2019
# Last Modified Date: 24th May 2019

class Parser:
    """
    This class extracts and encapsulates the components of an individual post.

    This class is instantiated with a line from the input file to extract it's ID, post type, creation
    date quarter, cleaned body and vocabulary size.

    Parameters:
    -----------
    inputString(str) ------> Contains a string in raw format from an xml file with the html tags/character-references.

    Attributes:
    -----------
    ID(int) ---------------> Row ID of inputString
    type(str) -------------> "Question","Answer" or "Others", based on the PostTypeId of the inputString
    dateQuarter(str) ------> A string that contains the year and quarter in which the post was created, example "2016Q1"
    cleanBody(str) --------> A clean version of inputString with all the html tags/character-references removed
    vocabularySize(int)----> The number of unique words used in a given cleanBody
    """

    def __init__(self, inputString):
        # Constructor, called to initialise the attributes
        self.inputString = inputString
        self.ID = self.getID()
        self.type = self.getPostType()
        self.dateQuarter = self.getDateQuarter()
        self.cleanBody = self.getCleanedBody()
        self.vocabularySize = self.getVocabularySize()

    def __str__(self):
        # String representation of the object. This method is called when print() function is invoked on this object.
        return "ID = {a}\nPOST TYPE = {b}\nCREATION DATE = {c}\nCLEANED CONTENT = {d}\nVOCABULARY SIZE = {e}" \
            .format(a=self.ID, b=self.type, c=self.dateQuarter, d=self.cleanBody, e=self.vocabularySize)

    def getID(self):
        # Method to return the row ID of inputString
        import re                                               # Importing regular expressions module
        ID = re.search(r'row Id="([0-9]+)"', self.inputString)  # Searching for the specified pattern in inputString
        return int(ID.group(1))                                 # Return the captured match of pattern in int converted form after search

    def getPostType(self):
        # Method to return a string "Question", "Answer" or "Others" to classify the type of post
        import re                                               # Importing regular expressions module
        type = re.search(r'PostTypeId="([0-9]+)"',
                         self.inputString)                      # Searching for the specified pattern in inputString
        if int(type.group(1)) == 1:
            return "Question"                                   # Returning the string "Question" if PostTypeId is 1
        elif int(type.group(1)) == 2:
            return "Answer"                                     # Returning the string "Answer" if PostTypeId is 2
        elif 3 <= int(type.group(1)) <= 8:
            return "Others"                                     # Returning the string "Others" if PostTypeId is between 3 and 8

    def getDateQuarter(self):
        # Method to return the year and quarter of the inputString based on the creation date
        import re                                               # Importing regular expressions module
        dateQuarter = re.search(r'CreationDate="([0-9].+)T',
                                self.inputString)               # Searching for the specified pattern in inputString
        date = dateQuarter.group(1)                             # Captured match of the pattern string after search
        dateList = date.split("-")                              # Split the string to a list with '-' as delimiter to separate Year and Month

        if 1 <= int(dateList[1]) <= 3:
            return dateList[0] + "Q1"                           # Month 1 to 3 : Q1, which is appended to Year from the list dateList
        elif 4 <= int(dateList[1]) <= 6:
            return dateList[0] + "Q2"                           # Month 4 to 6 : Q2, which is appended to Year from the list dateList
        elif 7 <= int(dateList[1]) <= 9:
            return dateList[0] + "Q3"                           # Month 7 to 9 : Q3, which is appended to Year from the list dateList
        elif 10 <= int(dateList[1]) <= 12:
            return dateList[0] + "Q4"                           # Month 10 to 12 : Q4, which is appended to Year from the list dateList

    def getCleanedBody(self):
        # Method to return a string with all the html tags/character-references removed
        from preprocessData_30281229 import preprocessLine      # Import function preprocessLine from file preprocessData_30281229
        return preprocessLine(self.inputString)                 # Return the output of the imported function preprocessLine, with paramter inputString

    def getVocabularySize(self):
        # Method to return the Vocabulary size i.e the count of unique words in cleanBody
        import re                                               # Importing regular expressions module
        removedspecialchars = re.sub('[^A-Za-z0-9 /]+', '',
                                     self.cleanBody).lower()    # Replacing the characters in cleanBody with the specified pattern
        wordCount = list(set(removedspecialchars.split()))      # Removing duplicate occurences of a word, using set and converting it to a list to get unique words
        return len(wordCount)                                   # Return the count of the list wordCount