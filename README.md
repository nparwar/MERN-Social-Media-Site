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

Usage
Launch the application.
Upload a PDF file containing event information.
Input the type of events you wish to extract.
The application will process the text, extract relevant events, and upload them to your Google Calendar.

Getting API Keys
To use the PDF Event Extractor, you need to obtain API keys for both Cohere and Google Calendar. These keys enable the application to interact with the respective services.

Cohere API Key
Sign up for Cohere: Create an account on Cohere's website.
Generate an API Key: Once your account is set up, navigate to the dashboard and generate an API key.
Configure the API Key in the Application: Add this key to your environment variables or directly into the application's configuration.

Google Calendar API Key
Google Cloud Console: Go to the Google Cloud Console.
Create a New Project: If you haven’t already, create a new project.
Enable the Calendar API: In the API & Services section, enable the Google Calendar API for your project.
Create Credentials: Go to the Credentials page and create credentials for your project. Choose 'OAuth client ID' and follow the setup process.
Download the Credentials: Once your credentials are created, download the JSON file and store it securely.
Configure the Credentials in the Application: Use these credentials in your application as specified in the installation instructions.
