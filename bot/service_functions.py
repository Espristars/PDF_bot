import tabula.io as tabula
import pandas
import json
import re
import os

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