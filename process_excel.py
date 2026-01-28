import pandas as pd
import json
import os

def process_excel():
    excel_path = 'Checklist_Adrenalyn_XL_2025-26.xlsx'
    output_path = 'data/adrenalyn_data.json'
    
    if not os.path.exists(excel_path):
        print(f"❌ Error: No se encuentra el archivo {excel_path}")
        return

    print(f"📖 Procesando {excel_path}...")
    xl = pd.ExcelFile(excel_path)
    
    # 1. Procesar Resumen
    resumen = []
    if 'RESUMEN' in xl.sheet_names:
        df_res = pd.read_excel(xl, 'RESUMEN', header=1)
        for _, row in df_res.iterrows():
            if pd.notna(row.iloc[0]) and "TOTAL" not in str(row.iloc[0]).upper():
                resumen.append({
                    "categoria": str(row.iloc[0]),
                    "total": int(row.iloc[1]) if pd.notna(row.iloc[1]) else 0,
                    "tengo": int(row.iloc[2]) if pd.notna(row.iloc[2]) else 0,
                    "progreso": round(float(row.iloc[4]) * 100, 1) if pd.notna(row.iloc[4]) else 0
                })

    # 2. Procesar Cartas
    hojas = [
        ('REGULARES', 'REGULAR'), ('Estadios', 'ESTADIO'), 
        ('¡VAMOS! (361–380)', '¡VAMOS!'), ('Guantes de Oro (381–387)', 'GUANTES DE ORO'),
        ('Kryptonita (388–396)', 'KRYPTONITA'), ('Diamantes (397–414)', 'DIAMANTE'),
        ('Influencers (415–423)', 'INFLUENCER'), ('Protas (424–441)', 'PROTA'),
        ('Super Cracks (442–467)', 'SUPER CRACK'), ('Cartas Top y Únicas (468–478)', 'TOP/ÚNICA')
    ]

    cartas = []
    for nombre_hoja, cat in hojas:
        if nombre_hoja in xl.sheet_names:
            df = pd.read_excel(xl, nombre_hoja)
            for _, row in df.iterrows():
                try:
                    val_id = str(row.iloc[0])
                    if val_id.isdigit():
                        tengo_val = str(row.iloc[3]).upper() if pd.notna(row.iloc[3]) else ""
                        cartas.append({
                            "id": int(val_id),
                            "nombre": str(row.iloc[1]),
                            "equipo": str(row.iloc[2]),
                            "categoria": cat,
                            "tengo": "SI" in tengo_val or "X" in tengo_val,
                            "repetidos": int(row.iloc[4]) if pd.notna(row.iloc[4]) else 0
                        })
                except: continue

    # Guardar
    os.makedirs('data', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({"resumen": resumen, "cartas": cartas, "actualizado": pd.Timestamp.now().strftime("%d/%m/%Y %H:%M")}, f, ensure_ascii=False)
    print(f"✅ JSON generado: {len(cartas)} cartas.")

if __name__ == "__main__":
    process_excel()
