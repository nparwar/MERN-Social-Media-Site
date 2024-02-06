# PDF Extractor

Description
PDF Event Extractor is a Python application designed to extract event information from PDF documents and upload it to a Google Calendar. It utilizes natural language processing and the Google Calendar API to identify and manage event data efficiently.

Features
PDF Reading: Leverages PyPDF2 for reading and extracting text from PDF documents.
Natural Language Processing: Utilizes cohere for natural language processing to interpret and structure the text data.
Event Extraction: Employs regular expressions and custom algorithms to identify event details from the text.
Google Calendar Integration: Uses the Google Calendar API to upload and manage events directly from the extracted data.
User Interface: Features a simple and interactive interface built with streamlit, making it accessible and easy to use.
Text Splitting: Implements langchain's CharacterTextSplitter for efficient text chunking and processing.
Technology Stack
Python
PyPDF2
Streamlit
Cohere
Langchain
Google Calendar API
Regular Expressions
Dotenv for environment variable management
Installation Instructions
Clone the repository to your local machine.
Install the required dependencies: pip install -r requirements.txt.
Set up your environment variables for Cohere API and Google Calendar credentials.
Run the application using Streamlit: streamlit run app.py.
Usage
Launch the application.
Upload a PDF file containing event information.
Input the type of events you wish to extract.
The application will process the text, extract relevant events, and upload them to your Google Calendar.
