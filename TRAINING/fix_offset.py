import json
import re

line_nums = [233, 237, 240, 242, 245, 249, 250, 251, 252, 260, 269, 271, 277, 278, 279,
303, 306, 307, 310, 314, 317, 320, 324, 327, 331, 332, 341, 343, 351, 362,
368, 371, 375, 376, 377, 379, 387, 398, 404, 413, 416, 417, 423, 429, 433,
436, 439, 444, 446, 447, 448, 459, 477, 479, 480, 484, 490, 498, 502, 510,
515, 517, 528, 530, 534, 536, 539, 545, 546, 550, 555, 556, 561, 570, 574
]

print(f'Najdenih {len(line_nums)} problematičnih vrstic.')
def safe_load_json(s: str, idx: int):
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        # poskušamo popraviti odvečne vejice pred ] ali }
        fixed = re.sub(r',\s*([\]}])', r'\1', s)
        try:
            return json.loads(fixed)
        except json.JSONDecodeError:
            print(f"[WARNING] Ne morem razvozljati JSON na vrstici {idx}: {e}")
            return None
# 2) Odpri JSONL in zapiši popravke
src_jsonl  = 'D:\\faks\\fri-fu\\diploma\\aplikacija\\TRAINING\\train_data4.jsonl'
out_jsonl  = 'train_data_fix4.jsonl'

with open('D:\\faks\\fri-fu\\diploma\\aplikacija\\TRAINING\\train_data4.jsonl', encoding='utf-8') as fin, \
    open(out_jsonl, 'w', encoding='utf-8') as fout:

    for idx, raw in enumerate(fin, start=1):
        data = safe_load_json(raw, idx)
        if data is None:
            # če ne moremo naložiti, preprosto prepišemo original
            fout.write(raw)
            continue

        if idx in line_nums and 'ents' in data and isinstance(data['ents'], list):
            new_ents = []
            for ent in data['ents']:
                if len(ent) >= 3 and isinstance(ent[0], int) and isinstance(ent[1], int):
                    new_start = ent[0] - 1
                    new_end   = ent[1] - 1
                    new_ents.append([new_start, new_end, ent[2]])
                else:
                    # če ent ni v pričakovani obliki, ga pustiš takšnega
                    new_ents.append(ent)
            data['ents'] = new_ents
            print(f"Vrstica {idx}: ents popravljeni na {new_ents}")

        fout.write(json.dumps(data, ensure_ascii=False) + '\n')

print("Popravek končan, rezultat v output.jsonl.")