import pandas as pd

def primerjaj_excel(f1, f2, output_excel="primerjava.xlsx"):
    # Naloži oba excela
    df1 = pd.read_excel(f1)
    df2 = pd.read_excel(f2)

    # Določi "ključ" za primerjavo – priporočam te stolpce:
    primerjaj_stolpce = ["doc_id", "sentence", "entity_text", "start_char", "end_char", "pred_label"]

    # Pretvori v string za primerjavo (tuple je najbolj robusten)
    df1["KEY"] = df1[primerjaj_stolpce].astype(str).agg("|".join, axis=1)
    df2["KEY"] = df2[primerjaj_stolpce].astype(str).agg("|".join, axis=1)

    set1 = set(df1["KEY"])
    set2 = set(df2["KEY"])

    # Zadetki, ki so v obeh modelih (intersekcija)
    skupni = set1 & set2

    # Novi zadetki v df2 (nova napoved, ki je prej ni bilo)
    novi = set2 - set1

    # Zadetki, ki jih je novi model izgubil (so bili, pa jih zdaj ni več)
    izgubljeni = set1 - set2

    # Export za preglednost (po želji)
    skupni_df = df2[df2["KEY"].isin(skupni)]
    novi_df = df2[df2["KEY"].isin(novi)]
    izgubljeni_df = df1[df1["KEY"].isin(izgubljeni)]

    # Shrani v več zavihtkov
    with pd.ExcelWriter(output_excel) as writer:
        skupni_df.to_excel(writer, sheet_name="SKUPNI", index=False)
        novi_df.to_excel(writer, sheet_name="NOVI", index=False)
        izgubljeni_df.to_excel(writer, sheet_name="IZGUBLJENI", index=False)

    print(f"Shranjeno v {output_excel}")
    print(f"Skupnih: {len(skupni_df)}")
    print(f"Novih: {len(novi_df)}")
    print(f"Izgubljenih: {len(izgubljeni_df)}")

# PRIMER UPORABE:
primerjaj_excel("errorlog6.xlsx", "errorlog6-2.xlsx", "primerjava6.xlsx")
