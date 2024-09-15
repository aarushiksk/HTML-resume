from PyPDF2 import PdfReader

import google.generativeai as genai
import os

# api_key=input("Enter your API key: ")
# genai.configure(api_key=api_key)

reader = PdfReader("D:\\Projects\\HTML resume maker\\Prodile_Rudra.pdf")
number_of_pages = len(reader.pages)

all_text=""
for i in range(number_of_pages):
    page = reader.pages[i]
    all_text+= page.extract_text()
    

    
list=indexs(all_text)
contact_text=contact_text(list)
skills_text=skills_text(list)
certifications_text=certifications_text(list)
name_text=name_text(list)
summary_text=summary_text(list)
experience_text=experience_text(list)
education_text=education_text(list)


# model = genai.GenerativeModel("gemini-1.5-flash")

# response = model.generate_content('''
# You are an expert AI assistant that takes in contents of resume and generates a only HTML resume.  Stick to below points
# 1) **UI/UX Design**:
# - Use fonts and colors that are ATS friendly and advisable.
# - It should look professional and clean.
# - Visuals should be appealing and easy to read.

# Include the following sections in the resume:
# 1) Name: ''' + name_text + '''
# - Top of the resume, bigger font size, information below in smaller size

# 2) Contact Information: ''' + contact_text + '''
# - Just below Name but above the rest of the resume, no need to make it too big, but should be easily visible

# 3) Education: ''' + education_text + '''

# 4) Summary: ''' + summary_text + ''' properly formatted

# 5) Skills: ''' + skills_text + ''' properly formatted

# 6) Experience: ''' + experience_text + ''' properly formatted

# 7) Certifications: ''' + certifications_text + ''' properly formatted

# 8) Do not generate explanations or any unecessary text
# ''')
# print(response.text)





prompting='''You are an expert AI assistant that takes in contents of resume and generates a only HTML resume.  Stick to below points
 1) **UI/UX Design**:
- Use fonts that are ATS friendly and advisable.
- Texts should not be too big
- It should look professional and clean.
- Visuals should be appealing and easy to read.
- It must be properly formatted and structured.
- Usage of standard fonts and colors is recommended.
- No usage of any extra comments lines, only the resume content should be generated.

Include the following sections in the resume:
1) Name: ''' + name_text + '''
- Top of the resume, bigger font size, information below in smaller size

2) Contact Information: ''' + contact_text + '''
- Just below Name but above the rest of the resume, no need to make it too big, but should be easily visible

3) Education: ''' + education_text + '''

4) Summary: ''' + summary_text + ''' properly formatted

5) Skills: ''' + skills_text + ''' properly formatted

6) Experience: ''' + experience_text + ''' properly formatted

7) Certifications: ''' + certifications_text + ''' properly formatted

8) Do not generate explanations or any unecessary text'''





from groq import Groq


GROQ_API_KEY = input("Enter your GROQ API key: ")
client = Groq(
    api_key=GROQ_API_KEY,
)


chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "you are an expert AI assistant that helps users build HTML resumes from text provided in a good manner. You have to generate a only HTML resume from the text provided in the following format",
        },
        {
            "role": "user",
            "content":prompting,
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)


