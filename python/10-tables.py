import boto3 
import os
from dotenv import load_dotenv
from trp import Document
load_dotenv()

os.environ['AWS_DEFAULT_REGION'] = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
os.environ['AWS_ACCESS_KEY_ID'] = os.getenv("AWS_ACCESS_KEY_ID")
os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv("AWS_SECRET_ACCESS_KEY")

# Document
documentName = "employmentapp.png"

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

for page in doc.pages:
     # Print tables
    for table in page.tables:
        for r, row in enumerate(table.rows):
            for c, cell in enumerate(row.cells):
                print("Table[{}][{}] = {}".format(r, c, cell.text))


'''
Table[0][0] = Applicant 
Table[0][1] = Information
Table[1][0] = Full Name: Jane
Table[1][1] = Doe
Table[2][0] = Phone Number:
Table[2][1] = 555-0100
Table[3][0] = Home Address:
Table[3][1] = 123 Any Street, Any Town, USA
Table[4][0] = Mailing Address:
Table[4][1] = same as home address
Table[0][0] =
Table[0][1] =
Table[0][2] = Previous Employment
Table[0][3] = History
Table[0][4] =
Table[1][0] = Start Date
Table[1][1] = End Date
Table[1][2] = Employer Name
Table[1][3] = Position Held
Table[1][4] = Reason for leaving
Table[2][0] = 1/15/2009
Table[2][1] = 6/30/2011
Table[2][2] = Any Company
Table[2][3] = Assistant Baker
Table[2][4] = Family relocated
Table[3][0] = 7/1/2011
Table[3][1] = 8/10/2013
Table[3][2] = Best Corp.
Table[3][3] = Baker
Table[3][4] = Better opportunity
Table[4][0] = 8/15/2013
Table[4][1] = present
Table[4][2] = Example Corp.
Table[4][3] = Head Baker
Table[4][4] = N/A, current employer

'''