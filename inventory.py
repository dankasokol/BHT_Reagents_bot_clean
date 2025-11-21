import pandas as pd

DF = pd.read_excel("Реактивы.xlsx", sheet_name="Реактивы")

def search_reagents(query: str, max_results=10):
    q = query.strip()
    if not q:
        return DF.iloc[0:0]

    mask1 = DF["Название"].fillna("").str.contains(q, case=False)
    mask2 = DF["Формула"].fillna("").str.contains(q, case=False)
    mask3 = DF["Торговое/альтерн название"].fillna("").str.contains(q, case=False)

    res = DF[mask1 | mask2 | mask3]
    return res.head(max_results)

# Форматирование результата для ответа
def format_reagent(row):
    name = row.get("Название", "")
    formula = row.get("Формула", "")
    trade = row.get("Торговое/альтерн название", "")
    pack = row.get("Фасовка", "")
    qty = row.get("Количество", "")
    lab = row.get("Лаборатория", "")
    cupboard = row.get("Шкаф", "")
    shelf = row.get("Полка", "")
    label = row.get("Этикетка", "")

    text = f"🔹 <b>{name}</b>"
    if pd.notna(formula):
        text += f" ({formula})"

    if pd.notna(trade):
        text += f"\n💬 Альтернативное: {trade}"

    if pd.notna(pack):
        text += f"\n📦 Фасовка: {pack}"

    if pd.notna(qty):
        text += f"\n🔢 Количество: {qty}"

    loc = []
    if pd.notna(lab):
        loc.append(f"Лаборатория: {lab}")
    if pd.notna(cupboard):
        loc.append(f"Шкаф: {cupboard}")
    if pd.notna(shelf):
        loc.append(f"Полка: {shelf}")
    if pd.notna(label):
        loc.append(f"Этикетка: {label}")

    if loc:
        text += "\n📍 " + " | ".join(loc)

    return text
