import boto3
import os
from trp import Document
from tabulate import tabulate

from dotenv import load_dotenv
from trp import Document
load_dotenv()

os.environ['AWS_DEFAULT_REGION'] = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
os.environ['AWS_ACCESS_KEY_ID'] = os.getenv("AWS_ACCESS_KEY_ID")
os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv("AWS_SECRET_ACCESS_KEY")



#create a Textract Client
textract = boto3.client('textract')
#Document
image_filename = "verification-of-employment.png"
response = None
with open(image_filename, 'rb') as document:
    imageBytes = bytearray(document.read())

# Call Textract AnalyzeDocument by passing a document from local disk
response = textract.analyze_document(
    Document={'Bytes': imageBytes},
    FeatureTypes=["FORMS",'SIGNATURES']
)

#print detected text
d = []
for item in response["Blocks"]:
    if item["BlockType"] == "SIGNATURE":
        d.append([item["Id"],item["Geometry"]])


print(tabulate(d, headers=["Id", "Geometry"], tablefmt="grid"))

 
doc = Document(response)
d = []

for page in doc.pages:
    # Search fields by key
    print("\nSearch Fields:")
    key = "Signature"
    fields = page.form.searchFieldsByKey(key)
    for field in fields:
        d.append([field.key, field.value])        

print(tabulate(d, headers=["Key", "Value"]))
