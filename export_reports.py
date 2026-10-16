import pandas as pd
import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf_report(report_title, data):
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()
    elements = [
        Paragraph(report_title, styles["Title"]),
        Spacer(1, 16),
        Paragraph(
            f"Report rows: {len(data)}",
            styles["Normal"]
        ),
        Spacer(1, 12)
    ]

    table_data = [data.columns.astype(str).tolist()]
    for row in data.head(100).itertuples(index=False, name=None):
        table_data.append([
            str(value)[:40] for value in row
        ])

    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.lightgrey])
    ]))

    elements.append(table)
    document.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


st.set_page_config(
    page_title="RetailPulse Export Reports",
    page_icon="📊",
    layout="wide"
)

st.title("RetailPulse - Export Reports")
st.write("Download project data as CSV or PDF reports.")

reports = {
    "Cleaned Sales Data": "retailpulse_cleaned.csv",
    "Customer RFM Data": "retailpulse_rfm.csv",
    "Customer Clusters": "retailpulse_clusters.csv",
    "Churn Summary": "retailpulse_churn_summary.csv",
    "Inventory Summary": "retailpulse_inventory_summary.csv",
    "Forecast Comparison": "retailpulse_forecast_comparison.csv",
    "Monitoring Summary": "retailpulse_monitoring_summary.csv"
}

selected_report = st.selectbox(
    "Select a report",
    list(reports.keys())
)

try:
    data = pd.read_csv(reports[selected_report])

    st.subheader(selected_report)
    st.write(f"Rows: {len(data):,} | Columns: {len(data.columns)}")
    st.dataframe(data.head(20), use_container_width=True)

    csv_data = data.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download CSV",
        data=csv_data,
        file_name=selected_report.lower().replace(" ", "_") + ".csv",
        mime="text/csv"
    )

    pdf_data = create_pdf_report(selected_report, data)

    st.download_button(
        "Download PDF",
        data=pdf_data,
        file_name=selected_report.lower().replace(" ", "_") + ".pdf",
        mime="application/pdf"
    )

except FileNotFoundError as e:
    st.error(f"Report file not found: {e.filename}")
    st.info(
        "Make sure the required CSV files are saved "
        "in the RetailPulse project folder."
    )

except Exception as e:
    st.error("Could not generate the report.")
    st.code(str(e))