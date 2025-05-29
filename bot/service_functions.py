import tabula.io as tabula
import pandas
import json
import re
import os
from PIL import Image
import pytesseract

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


async def file_convert_photo_to_text(path_file: str) -> str:

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    text = pytesseract.image_to_string(Image.open(path_file), lang="rus+eng")

    filename = await file_convert_text_to_json(text)

    return filename


async def file_convert_text_to_json(text: str) -> str:
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]

    client_id_idx = lines.index("client_id")
    fio_idx = lines.index("client_FlO")
    income_idx = lines.index("credit_income")

    client_ids = [line.replace(" ", "") for line in lines[client_id_idx + 1:client_id_idx + 6]]
    fios = lines[fio_idx + 1:fio_idx + 6]
    incomes = lines[income_idx + 1:income_idx + 6]

    result = []
    for i in range(5):
        result.append({
            client_ids[i]: {
                "client_FIO": fios[i],
                "credit_income": float(incomes[i])
            }
        })

    filename = os.path.join("photos", "file.json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return filename