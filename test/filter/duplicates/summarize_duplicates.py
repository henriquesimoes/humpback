from collections import defaultdict

import pandas as pd


def filter(df):
    all = []

    for id, row in df.iterrows():
        ids = row['Duplicates'].split()
        ids = sorted(ids)

        all.append(' '.join(ids))

    all = list(set(all))
    all = sorted(all)

    return pd.DataFrame({'Duplicates': all})


def merge(df):
    id_dict = defaultdict(set)
    merged = False

    for id, row in df.iterrows():
        ids = row['Duplicates'].split()

        for new in ids[1:]:
            id_dict[ids[0]].add(new)

    for id, values in id_dict.items():
        add = set()
        for duplicate in values:
            if duplicate in id_dict:
                ext = list(id_dict[duplicate])

                merged = True

                for x in ext:
                    if x != id:
                        add.add(x)

        for x in add:
            id_dict[id].add(x)

    used = set()
    remove = set()
    for key, values in id_dict.items():
        if key not in remove:
            used.add(key)
            for v in values:
                if v not in used:
                    remove.add(v)

    for rm in remove:
        if rm in id_dict:
            print('removing', rm)
            del id_dict[rm]

    assert len(id_dict) == len(used)

    result = []
    for id, value in id_dict.items():
        result.append(' '.join(sorted([id] + list(value))))

    return pd.DataFrame({'Duplicates': result}), merged


def main():
    df = pd.read_csv('raw_duplicates.csv').set_index("Id")
    merged = True

    while merged:
        df = filter(df)
        df, merged = merge(df)

    df.to_csv('duplicates.csv')


if __name__ == "__main__":
    main()
