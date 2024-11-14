import boto3 
import os
from dotenv import load_dotenv
from trp import Document
load_dotenv()

os.environ['AWS_DEFAULT_REGION'] = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
os.environ['AWS_ACCESS_KEY_ID'] = os.getenv("AWS_ACCESS_KEY_ID")
os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv("AWS_SECRET_ACCESS_KEY")

# Document
documentName = "expense.png"

# Amazon Textract client
textract = boto3.client('textract')

# Call Amazon Textract
with open(documentName, "rb") as document:
    response = textract.analyze_document(
        Document={
            'Bytes': document.read(),
        },
        FeatureTypes=["TABLES"])

#print(response)

doc = Document(response)

def isFloat(input):
  try:
    float(input)
  except ValueError:
    return False
  return True

warning = ""
for page in doc.pages:
     # Print tables
    for table in page.tables:
        for r, row in enumerate(table.rows):
            itemName  = ""
            for c, cell in enumerate(row.cells):
                print("Table[{}][{}] = {}".format(r, c, cell.text))
                if(c == 0):
                    itemName = cell.text
                elif(c == 4 and isFloat(cell.text)):
                    value = float(cell.text)
                    if(value > 1000):
                        warning += "{} is greater than $1000.".format(itemName)
if(warning):
    print("\nReview needed:\n====================\n" + warning)
'''

Table[0][0] = 
Table[0][1] =
Table[0][2] = Expense Report
Table[0][3] =
Table[0][4] =
Table[1][0] = Expense Description
Table[1][1] = Type
Table[1][2] = Date
Table[1][3] = Merchant Name
Table[1][4] = Amount (USD)
Table[2][0] = Furniture (Desks and Chairs)
Table[2][1] = Office Supplies
Table[2][2] = 5/10/1019
Table[2][3] = Merchant One
Table[2][4] = 1500.00
Table[3][0] = Team Lunch
Table[3][1] = Food
Table[3][2] = 5/11/2019
Table[3][3] = Merchant Two
Table[3][4] = 100.00
Table[4][0] = Team Dinner
Table[4][1] = Food
Table[4][2] = 5/12/2019
Table[4][3] = Merchant Three
Table[4][4] = 300.00
Table[5][0] = Laptop
Table[5][1] = Office Supplies
Table[5][2] = 5/13/2019
Table[5][3] = Merchant Three
Table[5][4] = 200.00
Table[6][0] =
Table[6][1] =
Table[6][2] =
Table[6][3] =
Table[6][4] =
Table[7][0] =
Table[7][1] =
Table[7][2] =
Table[7][3] =
Table[7][4] =
Table[8][0] =
Table[8][1] =
Table[8][2] =
Table[8][3] =
Table[8][4] =
Table[9][0] =
Table[9][1] =
Table[9][2] =
Table[9][3] = Total
Table[9][4] = 2100.00

'''