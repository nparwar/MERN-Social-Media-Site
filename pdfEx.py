from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
import streamlit as st
import cohere
import re
from langchain.text_splitter import CharacterTextSplitter
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import asyncio


# Load environment variables
load_dotenv()

client_id = os.environ['GOOGLE_CLIENT_ID']
client_secret = os.environ['GOOGLE_CLIENT_SECRET']
redirect_uri = os.environ['REDIRECT_URI']
co = cohere.Client(os.environ["COHERE_API_KEY"])
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def process_text(text):
    # Split the text into chunks using Langchain's CharacterTextSplitter
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    return chunks

def upload(events, creds):
    try:
      service = build("calendar", "v3", credentials=creds)

      # Call the Calendar API
      for i in events:
        date_string = i[0].strip()
        final_date = date_string.replace("/", "-")

        # Get the current year
        current_year = datetime.datetime.now().year

        # Combine the current year with the date string
        full_date_string = f"{current_year}-{final_date}"

        event = {
            'summary': i[1],
            'start': {'date': full_date_string},
            'end': {'date': full_date_string}
        }
        service.events().insert(calendarId='primary', body=event).execute()
      
    except HttpError as error:
        print(f"An error occurred: {error}")

def main():
    st.title("PDF Extractor")

    creds = None
    # Check if token.json exists
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # Try to refresh or fetch new token if needed
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = Flow.from_client_secrets_file(
            "credentials.json",
            scopes=SCOPES,
            redirect_uri="https://pdf-extractor.streamlit.app/"
        )

        # Check if we are being redirected back with the code
        query_params = st.experimental_get_query_params()
        auth_url, _ = flow.authorization_url(prompt='consent')
        st.write(f"Please go to this URL and authorize access: {auth_url}")
        query_params = st.experimental_get_query_params()
        
            # Use the code from the query params to fetch the token
        code = query_params['code'][0]  # Extract the code
        flow.fetch_token(code=code)
        creds = flow.credentials
            # Save the credentials for future use
        with open("token.json", "w") as token_file:
            token_file.write(creds.to_json())



          

    pdf = st.file_uploader('Upload your PDF document', type='pdf')

    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        docs = process_text(text)

        query = st.text_input('Enter what events you wish to extract from your pdf')
        cancel_button = st.button('Cancel')

        if cancel_button:
            st.stop()

        if query:
            orderedDocs = co.rerank(
            model = 'rerank-english-v2.0',
            query = 'Find all ' + query,
            documents = docs,
            top_n = 10,
            )
            finalDocs = [{"id" : str(i.index), "text" : str(docs[i.index])} for i in orderedDocs if i.relevance_score > .5]
            response = co.chat(
                model="command",
                message="Return a list of " + query + " from the document. Format the results in a list with the date followed by a space and then the assignment name. Each date assignment pair should be separated by a comma. Here is an example: [09/12 HW1, 05/12 HW2, etc.]",
                documents=finalDocs)
            
            st.write(response.text)

            # Extract the assignments part
            start_index = response.text.find('[')
            assignments_str = response.text[start_index:].strip('[]')

            # Split the string into individual assignments
            assignments = assignments_str.split(', ')

            # Initialize a list to hold the result
            assignment_list = []

            # Process each assignment
            for assignment in assignments:
                # Use regex to find the date
                match = re.search(r'\d{1,2}/\d{1,2}', assignment)
                if match:
                    date = match.group()
                    description_start = match.end()
                    description = assignment[description_start:].strip()
                    assignment_list.append((date, description))

            # Print or return the result
            for item in assignment_list:
                print(item)
            upload(assignment_list, creds)
            print(response)

if __name__ == "__main__":
    main()
