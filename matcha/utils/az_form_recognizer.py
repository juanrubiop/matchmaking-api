#---------- Imports for skill extraction
import os
from os import listdir
from os.path import isfile, join
import base64
import sys
import io
import re
from unidecode import unidecode
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentModelAdministrationClient, ModelBuildMode, DocumentAnalysisClient
from azure.core.exceptions import HttpResponseError

#----------

#----------- Functions for extraction
def create_helping_variables_dict():
    
    """
    create_helping_variables_dict
    
    Creates all the lists needed for proper extraction and text comprehension by importing them from files
    ___________________
    Arguments
    ___________________
    Returns
    
    result dictionary with the lists
    """
    stop_words_english=[]
    stop_words_spanish=[]
    technical_skills=[]
    path_stop_words_spanish="resources/spanish.txt"
    path_stop_words_english="resources/english.txt"
    path_skills="resources/linkedin_skills.txt"

    file=open(path_skills,'r')
    temp=file.read()
    temp=temp.replace('+','\+')
    temp=temp.replace('*','\*')
    technical_skills = temp.splitlines()
    file.close()

    file=open(path_stop_words_spanish,'r')
    temp=file.read()
    stop_words_spanish = temp.splitlines()
    file.close()

    file=open(path_stop_words_english,'r')
    temp=file.read()
    stop_words_english = temp.splitlines()
    file.close()

    return { 'stop_words_spanish':stop_words_spanish,
              'stop_words_english':stop_words_english,
              'technical_skills':technical_skills}

def check_azure_credentials(credentials):
    CUSTOM_BUILT_MODEL_ID=credentials['CUSTOM_BUILT_MODEL_ID']
    AZURE_FORM_RECOGNIZER_ENDPOINT=credentials['AZURE_FORM_RECOGNIZER_ENDPOINT']
    AZURE_FORM_RECOGNIZER_KEY=credentials['AZURE_FORM_RECOGNIZER_KEY']

    """
    check_azure_credentials
    Verifies that all credentials are valid before calling the function that calss the azure services
    ___________________
    Arguments

    credentials
    ___________________
    Returns
    
    result valid
    """
    
    try:
        valid=False
        if CUSTOM_BUILT_MODEL_ID:

            if not AZURE_FORM_RECOGNIZER_ENDPOINT or not AZURE_FORM_RECOGNIZER_KEY:
                raise ValueError("Please provide endpoint and API key to run the samples.")

            document_model_admin_client = DocumentModelAdministrationClient(
                endpoint=AZURE_FORM_RECOGNIZER_ENDPOINT, credential=AzureKeyCredential(AZURE_FORM_RECOGNIZER_KEY)
            )
            valid=True
        return valid
    
    except HttpResponseError as error:
        print("For more information about troubleshooting errors, see the following guide: "
              "https://aka.ms/azsdk/python/formrecognizer/troubleshooting")
        # Examples of how to check an HttpResponseError
        # Check by error code:
        if error.error is not None:
            if error.error.code == "InvalidImage":
                print(f"Received an invalid image error: {error.error}")
            if error.error.code == "InvalidRequest":
                print(f"Received an invalid request error: {error.error}")
            # Raise the error again after printing it
            raise
        # If the inner error is None and then it is possible to check the message to get more information:
        if "Invalid request".casefold() in error.message.casefold():
            print(f"Uh-oh! Seems there was an invalid request: {error}")
        # Raise the error again
        raise

def analyze_custom_documents(credentials, cv_base64_string):
    """
    ANALYEZE_CUSTOM_DOCUMENTS
    Takes the file and calls the azure service to analyze it
    ___________________
    Arguments

    CUSTOM_MODEL_ID[STring]
    cv_base64_string[base65]
    ___________________
    Returns

    result[result]
    """
    data_bytes = cv_base64_string.encode('utf-8')
    decoded_data = base64.decodebytes(data_bytes)
    file = io.BytesIO(decoded_data)

    document_analysis_client = DocumentAnalysisClient(endpoint=credentials['AZURE_FORM_RECOGNIZER_ENDPOINT'], credential=AzureKeyCredential(credentials['AZURE_FORM_RECOGNIZER_KEY']))

    poller = document_analysis_client.begin_analyze_document(model_id=credentials['CUSTOM_BUILT_MODEL_ID'], document=file)
    result = poller.result()

    return result

def extract_skills_from_text(output):

    """
    EXTRACT_SKILLS_FROM_TEXT
    Extracts the skill from the text output the azure service provides after calling it
    ___________________
    Arguments

    cv_base64_string[base64]
    ___________________
    Returns
    
    result hardskills[String]
    """

    pages_content=[]
    
    for page in output.pages:
        pages_content.append(' '.join(e.content for e in page.lines))

    file_content=' '.join(pages_content)
    file_content=" ".join([word for word in re.split("\W+",file_content)
                                  if word and word.lower() not in skills_language_parsing['stop_words_english']
                                          and word and word.lower() not in skills_language_parsing['stop_words_spanish']]
                            )  # filter out empty words
    
    hardskills = [skill for skill in skills_language_parsing['technical_skills']
                        if re.search(' ' + skill.lower() + ' ', file_content.lower())]
    return hardskills

def extract_skills_from_text_db(output,skill_list):

    """
    EXTRACT_SKILLS_FROM_TEXT
    Extracts the skill from the text output the azure service provides after calling it
    ___________________
    Arguments

    cv_base64_string[base64]
    ___________________
    Returns
    
    result hardskills[String]
    """

    pages_content=[]
    skill_list=[skill.replace('+','\+').replace('*','\*') for skill in skill_list]

    
    for page in output.pages:
        pages_content.append(' '.join(e.content for e in page.lines))

    file_content=' '.join(pages_content)
    file_content=" ".join([word for word in re.split("\W+",file_content)
                                  if word and word.lower() not in skills_language_parsing['stop_words_english']
                                          and word and word.lower() not in skills_language_parsing['stop_words_spanish']]
                            )  # filter out empty words
    
    hardskills = [skill for skill in skill_list
                        if re.search(' ' + skill.lower() + ' ', file_content.lower())]
    return hardskills

def extract_data_from_cv(result):
    name=[]
    parsed_names=[]
    address=[]
    phone=[]
    email=[]
    linkedin=[]
    parsed_linkedin=[]

    for idx, cv in enumerate(result.documents):
        name.append(cv.fields.get('Name').value)
        parsed_names.append("".join(ch for ch in cv.fields.get('Name').value if (ch.isalnum() or ch==' ')))
        address.append(cv.fields.get('Address').value)
        phone.append(cv.fields.get('Phone').value)
        email.append(cv.fields.get('E-Mail').value)
        linkedin.append(cv.fields.get('Linkedin').value)
        parsed_linkedin.append(re.findall(r'(?<=\s)www\..*', cv.fields.get('Linkedin').value))
    
        
    return {
        'names':name,
        'parsed_names':parsed_names,
        'address':address,
        'phones':phone,
        'emails':email,
        'linkedin':linkedin,
        'parsed_linkedin':parsed_linkedin
    }

skills_language_parsing = create_helping_variables_dict()
