### 🤖Flask based Resume HTML generator

###### ⚡This app uses Gemini model-1.5-flash and Groq, llama-3 for to generate HTML page content out LinkedIn generated PDF.

#### Process Flow Diagram:

<img src="">


#### Approach:

1) Utilizing Gemini and Groq APIs inside of OPENAI-API as they as they are free of cost.
2) Utilizing PyPDF to parse different sections of LinkedIn generated PDF like Skills, Experience, Education, Contact Information, etc...
3) Chain-of-thought prompting to chat template of groq llama3-8b-8192.
4) Allowing the user to download html content and run it locally

#### Folder structure: 
 - static: Contains css and js files
 - templates: Contains html templates
 - app py: Contains flask app
 - main.py: To check running of the app



