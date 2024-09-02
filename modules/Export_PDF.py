from fpdf import FPDF

def export_pdf(title, content):
    result = content.encode("latin-1", "replace").decode("latin-1")
    title_blog = title.encode("latin-1", "replace").decode("latin-1")

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Times", "B", size=16)
    pdf.cell(190, 10, txt = title_blog, align="C")

    pdf.set_x(10)
    pdf.set_y(25)

    pdf.set_font("Times", size=12)
    pdf.multi_cell(190, 5, txt = result, align="L")
    final = pdf.output(dest="S").encode("latin-1")
    final = pdf.output().encode("utf-8")
    
    return final