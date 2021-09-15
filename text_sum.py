## ---------------------------------------------------------
## Hello! I'm Victor G. and I code dinosaurs since 2003! :D
## ---------------------------------------------------------
##
## By Victor Rosa Gomez <vicg853@gmail.com>
## GH: https://github.com/Vicg853
## Mainly made for Mainha (Maya Moron Rajha) SZ SZ ;D, the best person in the whole world!!
##
## This file uses:
##   - summanlp's textrank A.I. model -> https://github.com/summanlp/textrank
##   - tkinter python interface -> https://docs.python.org/3/library/tkinter.html
##   - chrismattmann's tika -> https://github.com/chrismattmann/tika-python
##   - uuid -> https://docs.python.org/3/library/uuid.html
##   - uuid -> https://docs.python.org/3/library/uuid.html


#Simply importing necessary modules
import os, uuid, requests, json
from dotenv import load_dotenv
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tika import parser
from summa import keywords
from summa.summarizer import summarize
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions, ConceptsOptions

#Defining main vars
load_dotenv()
IBM_API_KEY_NL_ENV = os.getenv('IBM_API_KEY_NL')
IBM_URL_NL = os.getenv('IBM_URL_NL')
imb_authenticator_nl = IAMAuthenticator(str(IBM_API_KEY_NL_ENV))

#Opening file choosing dialog using tkinter
Tk().withdraw()
filename = askopenfilename()

#Opening file and reading it with tika
parsed_pdf=parser.from_file(filename)
text=parsed_pdf['content']
print('Cleaning up file...')
text=text.replace('\n', '').replace('\r', '').replace('"', ' ').replace("'", '')
pdf_name=parsed_pdf['metadata']['resourceName']
pdf_name=pdf_name[:-5]+str(uuid.uuid4())

#Asking what language and proportion of the text must the summary be will be used
print('----#### FOR SUMA ML ####----')
print('For Summa ML: Which language would you like to use for this text. The available ones are: arabic, danish, dutch, english, finnish, french, german, hungarian, italian, norwegian, polish, porter, portuguese, romanian, russian, spanish and swedish')
lang=input('Language: ')
print("For Summa ML: How long should the summary be, in a 0.0 to 1.0 scale?")
length=input('Size: ')
print(' ')
print(' ')
print('----#### FOR IBM NATURAL LANGUAGE ML ####----')
print("How many keywords would you like to get?")
ibm_ml_keywords_num=int(input('Number: '))
print("How many concepts explanation sources would you like to get?")
ibm_ml_concepts_num=int(input('Number: '))

#Printing file info and file saving names
print(' ')
print(' ')
print("Alright, I'm going to work on it... ")

print("The text's summary+keywords and etc will be exported into the folder 'results/", pdf_name, "'  !")

#Passing data to summa Model and getting summarized version + keywords
summary=summarize(text, language=lang, ratio=float(length))

#Making request to IBM Cloud Natural Language Summarization
ibm_nl_query=NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=imb_authenticator_nl)
ibm_nl_query.set_service_url(IBM_URL_NL)
ibm_nl_response=ibm_nl_query.analyze(text=text,features=Features(concepts=ConceptsOptions(limit=ibm_ml_concepts_num), keywords=KeywordsOptions(limit=ibm_ml_keywords_num))).get_result()
print(json.dumps(ibm_nl_response, indent=2))
ibm_nl_extrated_keywords=[]
ibm_nl_extracted_concepts=[]

#Creating files to save text and keywords
parent_path=os.getcwd()
full_path=parent_path+'/results/'+pdf_name

#Checking if directory already exists and creating it if not
if not os.path.exists(full_path):
    os.makedirs(full_path)

#Creating and writing data into files
with open(os.path.join(full_path, 'text_rank_summary_file.txt'), 'w+') as file :
	file.write("Summary made with summa python ML model (these in fact are just the most relevant sentences extrated out of the text, based on the size input given by the user): \n" + str(summary))

with open(os.path.join(full_path, 'text_keywords__file.txt'), 'w+') as file :
    file.write("Keywords extracted with IBM NL model (relevance ratio in a 0 to 1 sacale, e.g.: 0.4/1 ratio): \n")

    for keyword in ibm_nl_response['keywords']:
        file.write(" - Keyword: '" + str(keyword['text']) + "', having a " + str(keyword['relevance']) + " relevance ratio..." + "\n")

    file.write("\n \n \n \nConcepts extracted with IBM NL model (url at the side, is the link that should explain the relevant concept): \n")

    for concept in ibm_nl_response['concepts']:
        file.write(" - " + str(concept['text']) + ": " + str(concept['dbpedia_resource']) + "\n")



print('All done! Have a great time now that the text is summarized Mainha, beijins :D!!')
