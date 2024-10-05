

from fpdf import FPDF

response = """

// trial ( import the cleaned response from the main scripts to convert them to pdf's)

Your friend's sculpted or fine-tuned response text goes here. 
This can be a long string or multiple paragraphs.
It could be dynamic, depending on what you're trying to convert.
"""
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

response_lines = response.split('\n')
for line in response_lines:
    pdf.multi_cell(0, 10, txt=line)  
pdf.output("response.pdf")

