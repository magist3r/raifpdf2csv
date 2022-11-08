# importing required modules
import PyPDF2
import re
  
pdf_file = open('statement.pdf', 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_file)
  
parts = []
def visitor_body(text, cm, tm, fontDict, fontSize):
    parts.append(text)
       
for i in range(pdf_reader.numPages):
    page = pdf_reader.getPage(i)
    page.extract_text(visitor_text=visitor_body)

# convert multiline to the single line
text_body = "".join(line.strip() for line in "".join(parts).splitlines())

p_date = "(\d{2}.\d{2}.\d{4})"
p_sum = "(\d{0,3},?\d{0,3}\.\d{2})"
p_card = "(?:\d{4})?\s?"

p_groups = re.compile(f"{p_date} {p_date} {p_card}(.*?)\s?{p_sum} {p_sum} {p_sum} {p_sum}")
iterator = p_groups.finditer(text_body)
output = open('statement.csv', 'w', encoding="utf-8")
output.write("sep=|\n")
for m in iterator:
    for i in range(1, len(m.groups()) + 1):
        str = m.group(i)
        if i > 3:
            str = str.replace(",","").replace(".",",")

        output.write(f"{str}|")

    output.write("\n")

output.close()
pdf_file.close()