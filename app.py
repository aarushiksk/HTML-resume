from flask import Flask, render_template, request, redirect, url_for, send_file,abort
import os
from PyPDF2 import PdfReader
from groq import Groq
import google.generativeai as genai

app = Flask(__name__)



GENERATED_HTML_FOLDER = './generated_html'
app.config['GENERATED_HTML_FOLDER'] = GENERATED_HTML_FOLDER

if not os.path.exists(GENERATED_HTML_FOLDER):
    os.makedirs(GENERATED_HTML_FOLDER)

def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    number_of_pages = len(reader.pages)

    all_text = ""
    for i in range(number_of_pages):
        page = reader.pages[i]
        all_text += page.extract_text()
    
    return all_text

def indexs(text, name):
    contact = text.find("Contact")
    skills = text.find("Skills")
    certifications = text.find("Certifications")
    name_index = text.find(name)
    summary = text.find("Summary")
    experience = text.find("Experience")
    education = text.find("Education")
    
    return [contact, skills, certifications, name_index, summary, experience, education]

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        ai_model = request.form.get('ai_model')
        print(f"AI Model: {ai_model}")  # Debugging statement
        if not ai_model:
           
            return render_template('chatbot.html', error="AI model is required.")
        
        if ai_model.lower() == 'gemini':
            return redirect(url_for('index2'))
        else:
            return redirect(url_for('index'))
    return render_template('chatbot.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/index2')
def index2():
    return render_template('index2.html')



@app.route('/generate', methods=['POST'])
def generate_html():
    try:
        api_key = request.form['api_key']
        pdf_file = request.files['pdf']
        name = request.form['name_text']
        
        if pdf_file and pdf_file.filename.endswith('.pdf'):
            text = extract_text(pdf_file)
            
            index = indexs(text, name)
            
            contact_text = text[index[0]:index[1]-4]
            skills_text = text[index[1]:index[2]]
            certifications_text = text[index[2]:index[3]]
            name_text = text[index[3]:index[4]]
            summary_text = text[index[4]:index[5]]
            experience_text = text[index[5]:index[6]]
            education_text = text[index[6]:]
            
            prompting = f'''You are an expert AI assistant that takes in contents of resume and generates a only HTML resume. Stick to below points
            1) **UI/UX Design**:
            - Use fonts that are ATS friendly and advisable.
            - Texts should not be too big
            - It should look professional and clean.
            - Visuals should be appealing and easy to read.
            - It must be properly formatted and structured.
            - Usage of standard fonts recommended.
            - No usage of any extra comments lines, only the resume content should be generated.

            Include the following sections in the resume:
            1) Name: {name_text}
            - Top of the resume, bigger font size, information below in smaller size

            2) Contact Information: {contact_text}
            - Just below Name but above the rest of the resume, no need to make it too big, but should be easily visible

            3) Education: {education_text}

            4) Summary: {summary_text} properly formatted

            5) Skills: {skills_text} properly formatted

            6) Experience: {experience_text} properly formatted

            7) Certifications: {certifications_text} properly formatted

            8) Do not generate explanations or any unecessary text'''
            
            os.environ['GROQ_API_KEY'] = api_key
            client = Groq(api_key=api_key)

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "you are an expert AI assistant that helps users build HTML resumes from text provided in a good manner. You have to generate a only HTML resume from the text provided in the following format",
                    },
                    {
                        "role": "user",
                        "content": prompting,
                    }
                ],
                model="llama3-8b-8192",
            )
            generated_html_content = chat_completion.choices[0].message.content

            html_filename = f"{name}_resume.html"
            html_filepath = os.path.join(app.config['GENERATED_HTML_FOLDER'], html_filename)
            with open(html_filepath, 'w', encoding='utf-8') as html_file:
                html_file.write(generated_html_content)

            return redirect(url_for('download_file', filename=html_filename))
        else:
            error = "Invalid file format. Please upload a PDF file."
            return render_template('index.html', error=error)
    except Exception as e:
        print(f"Error: {e}")
        return render_template('index.html', error="An error occurred while processing your request.")
    
    
    
    
@app.route('/generategemini', methods=['POST'])
def gemini_generate():
    try:
        api_key = request.form['api_key']
        pdf_file = request.files['pdf']
        name = request.form['name_text']
        
        if pdf_file and pdf_file.filename.endswith('.pdf'):
            text = extract_text(pdf_file)
            
            index = indexs(text, name)
            
            contact_text = text[index[0]:index[1]-4]
            skills_text = text[index[1]:index[2]]
            certifications_text = text[index[2]:index[3]]
            name_text = text[index[3]:index[4]]
            summary_text = text[index[4]:index[5]]
            experience_text = text[index[5]:index[6]]
            education_text = text[index[6]:]
            
            prompting = f'''You are an expert AI assistant that takes in contents of resume and generates a only HTML resume. Stick to below points
            1) **UI/UX Design**:
            - Use fonts that are ATS friendly and advisable.
            - Texts should not be too big
            - It should look professional and clean.
            - Visuals should be appealing and easy to read.
            - It must be properly formatted and structured.
            - Usage of standard fonts recommended.
            - No usage of any extra comments lines, only the resume content should be generated.

            Include the following sections in the resume:
            1) Name: {name_text}
            - Top of the resume, bigger font size, information below in smaller size

            2) Contact Information: {contact_text}
            - Just below Name but above the rest of the resume, no need to make it too big, but should be easily visible

            3) Education: {education_text}

            4) Summary: {summary_text} properly formatted

            5) Skills: {skills_text} properly formatted

            6) Experience: {experience_text} properly formatted

            7) Certifications: {certifications_text} properly formatted

            8) Do not generate explanations or any unecessary text, no warnings anything extra'''
            
            
            genai.configure(api_key=api_key)
            os.environ['GEMINI_API_KEY'] = api_key
            model = genai.GenerativeModel("gemini-1.5-flash")
         
            response = model.generate_content(prompting)

            html_filename = f"{name}_resume.html"
            html_filepath = os.path.join(app.config['GENERATED_HTML_FOLDER'], html_filename)
            with open(html_filepath, 'w', encoding='utf-8') as html_file:
                html_file.write(response.text)

            return redirect(url_for('download_file', filename=html_filename))
        else:
            error = "Invalid file format. Please upload a PDF file."
            return render_template('index2.html', error=error)
        
    except Exception as e:
        print(f"Error: {e}")
        return render_template('index2.html', error="An error occurred while processing your request.")    
    
    
    
    

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.config['GENERATED_HTML_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            abort(404)
    except Exception as e:
        print(f"Error: {e}")
        return render_template('index2.html', error="An error occurred while trying to download the file.")

if __name__ == '__main__':
    app.run(debug=True)