import pandas as pd

# 1. naložimo Excel
df = pd.read_excel('D:\\faks\\fri-fu\\diploma\\aplikacija\\EXCEL\\četrtiposkuspopravljen.xlsx')

# 2. za vsako vrstico
for idx, row in df.iterrows():
    # Če manjkajo start/end (NaN)
    if pd.isna(row['start_char']) or pd.isna(row['end_char']):
        sentence = row['sentence']
        entity   = row['entity_text']
        
        # Preverimo, da sta oba nizova
        if not isinstance(sentence, str) or not isinstance(entity, str):
            # Po želji zabeležimo ali nastavimo na -1
            df.at[idx, 'start_char'] = -1
            df.at[idx, 'end_char']   = -1
            print(f"Vrstica {idx}: manjkajoči sentence ali entity_text, nastavljeno -1")
            continue
        
        # Poiščemo entiteto v sentence
        start = sentence.find(entity)
        if start != -1:
            end = start + len(entity)
            df.at[idx, 'start_char'] = start
            df.at[idx, 'end_char']   = end
            print(f"Vrstica {idx}: našel “{entity}” na {start}-{end}")
        else:
            # če ne najdemo
            df.at[idx, 'start_char'] = -1
            df.at[idx, 'end_char']   = -1
            print(f"Vrstica {idx}: entiteta “{entity}” ni najdena")
        