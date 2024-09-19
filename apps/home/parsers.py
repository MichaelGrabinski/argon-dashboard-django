from pdfminer.high_level import extract_text
import re

def parse_bank_statement_pdf(file):
    text = extract_text(file)
    transactions = []

    # Example regex pattern (adjust based on your statement format)
    pattern = re.compile(r'(\d{2}/\d{2}/\d{4})\s+([\w\s]+)\s+(-?\d+,\d{2})')

    for match in pattern.finditer(text):
        date_str = match.group(1)
        description = match.group(2).strip()
        amount_str = match.group(3)

        # Process date and amount formats as per your locale
        date = datetime.strptime(date_str, '%d/%m/%Y').date()
        amount = float(amount_str.replace(',', '.').replace(' ', ''))

        transactions.append({
            'date': date,
            'description': description,
            'amount': amount,
            # You can calculate balance or add more fields if available
        })
    return transactions