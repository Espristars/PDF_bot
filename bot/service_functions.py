import tabula.io as tabula
import pandas
import json
import re
import os
from PIL import Image
import pytesseract
import logging

logger = logging.getLogger()

def clean_numbers(x):
    x = re.sub(r'[^\d.]', '', str(x))
    return float(x)

async def file_convert_pdf_to_json(path_file: str) -> str:
    df = pandas.DataFrame(tabula.read_pdf(path_file, pages ='all')[0])

    df['credit_income'] = df['credit_income'].map(clean_numbers)

    result = []
    for _, row in df.iterrows():
        client = {
            row['client_id']:
                {
                    "client_FIO": row['client_FIO'],
                    "credit_income": row['credit_income']
                }
        }
        result.append(client)

    filename = os.path.join("documents", "file.json")

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return filename


async def file_convert_photo_to_text(path_file: str, index_col: int, index_str: int) -> str:

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    text = pytesseract.image_to_string(Image.open(path_file), lang="rus+eng")

    filename = await file_convert_text_to_json(text, index_col, index_str)

    return filename


async def file_convert_text_to_json(text: str, index_col: int, index_str: int) -> str:
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]

    if len(lines) != index_col * (index_str + 1):
        if len(lines) == index_str + 1:
            headers = re.split(r'\s+', lines[0])
            result = []

            for line in lines[1:]:
                parts = re.split(r'\s+', line, maxsplit=len(headers) - 1)
                if len(parts) != len(headers):
                    continue

                row = {}
                for key, value in zip(headers, parts):
                    try:
                        row[key] = float(value.replace(',', '.'))
                    except ValueError:
                        row[key] = value

                main_key = headers[0]
                key_value = row.pop(main_key)
                result.append({key_value: row})
        else:
            raise ValueError
    else:
        result = []
        columns = [lines[i * (index_str + 1):(i + 1) * (index_str + 1)] for i in range(index_col)]

        headers = [col[0] for col in columns]
        values_per_row = list(zip(*[col[1:] for col in columns]))

        for row in values_per_row:
            key = row[0]
            result.append({
                key: {
                    headers[i]: float(row[i]) if row[i].replace('.', '', 1).isdigit() else row[i]
                    for i in range(1, index_col)
                }
            })

    os.makedirs("photos", exist_ok=True)
    filename = os.path.join("photos", "file.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return filename