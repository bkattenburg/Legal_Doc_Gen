import streamlit as st
from jinja2 import Template
from faker import Faker
from fpdf import FPDF
import io
import datetime

fake = Faker()

# Example templates
templates = {
    "Appeal Document": """
    SPARK SERVICES V PENGUIN LLC - APPEAL DOCUMENT

    Matter: {{ matter_name }}
    Parties: {{ parties }}
    Date of Appeal: {{ appeal_date }}

    This Appeal concerns the denial of the plaintiff's motion for summary judgment. 
    The appellant argues the trial court erred due to {{ issue_detail }}.

    Requested relief: {{ relief }}
    """,

    "Deposition Transcript": """
    DEPOSITION TRANSCRIPT

    Matter: {{ matter_name }}
    Date: {{ dep_date }}
    Witness: {{ witness_name }}

    Q: Can you state your full name for the record?
    A: {{ witness_name }}

    Q: Please describe the events on {{ incident_date }}.
    A: {{ fake_paragraph }}
    """
}

# PDF creating function using fpdf2
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Spark Services v Penguin LLC - Sample Document", 0, 1, "C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

def render_to_pdf(text: str) -> bytes:
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf_output = pdf.output(dest='S').encode('latin1')  # returns bytes
    return pdf_output

st.title("ELM Sample Document Generator")

with st.form("doc_form"):
    matter_name = st.text_input("Matter Name", "Spark Services v Penguin LLC")
    parties = st.text_input("Parties", "Spark Services, Penguin LLC")
    appeal_date = st.date_input("Appeal Date", datetime.date.today())
    dep_date = st.date_input("Deposition Date", datetime.date.today())
    incident_date = st.date_input("Incident Date", datetime.date.today() - datetime.timedelta(days=30))
    witness_name = st.text_input("Witness Name", fake.name())
    issue_detail = st.text_area("Issue Detail for Appeal Document", "incorrect contract interpretation")
    relief = st.text_area("Relief Requested", "Reversal of summary judgment")
    doc_type = st.selectbox("Select Document Type", list(templates.keys()))

    submitted = st.form_submit_button("Generate Document")

if submitted:
    # Prepare data for template rendering
    data = {
        "matter_name": matter_name,
        "parties": parties,
        "appeal_date": appeal_date.strftime("%B %d, %Y"),
        "dep_date": dep_date.strftime("%B %d, %Y"),
        "incident_date": incident_date.strftime("%B %d, %Y"),
        "witness_name": witness_name,
        "issue_detail": issue_detail,
        "relief": relief,
        "fake_paragraph": fake.paragraph(nb_sentences=3)
    }

    template_text = templates[doc_type]
    template = Template(template_text)
    document_text = template.render(**data)

    # Generate PDF bytes
    pdf_bytes = render_to_pdf(document_text)

    st.subheader(f"Generated {doc_type}")
    st.text_area("Document Preview:", document_text, height=300)

    # Provide download link
    st.download_button(
        label="Download PDF",
        data=pdf_bytes,
        file_name=f"{doc_type.replace(' ', '_')}_Sample.pdf",
        mime="application/pdf",
    )
