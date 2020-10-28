from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pandas as pd


class DuplicateProcessing():
    def __init__(self, images=None, classes=None):
        self.df_images = pd.read_csv(images) if images is not None else None
        self.df_classes = pd.read_csv(classes) if classes is not None else None

    def apply(self, df):
        df = self._fix_images(df)
        df = self._fix_classes(df)

        return df

    def _fix_images(self, df):
        if self.df_images is None:
            return df

        for idx, row in self.df_images.iterrows():
            id = df.loc[row['Remove']]['Id']

            if df.loc[row['Keep']]['Id'] is not 'new_whale':
                id = df.loc[row['Keep']]['Id']

            df = df.drop(row['Remove'], errors='ignore')
            df.loc[row['Keep']]['Id'] = id

        return df

    def _fix_classes(self, df):
        if self.df_classes is not None:
            df_filter = self.df_classes[self.df_classes['Verdict'] == True]

            for idx, row in df_filter.iterrows():
                classes = row['Duplicates'].split()
                representant = classes[0]

                for i in range(1, len(classes)):
                    df.loc[df['Id'] == classes[i], 'Id'] = representant

        return df


def test_duplicate_images():
    duplicate = DuplicateProcessing(images=None, classes=None)

    other = ['other.jpg']
    keep = ['keep.jpg']
    remove = ['remove.jpg']
    duplicate.dfimages = pd.DataFrame({'Keep': keep, 'Remove': remove})

    df = pd.DataFrame({'Image': keep + other + remove, 'Id': ['new_whale'] + list('bc')})
    df = df.set_index('Image')

    assert len(df) == 3

    df = duplicate.apply(df)

    assert len(df) == 2
    assert other[0] in df.index
    assert keep[0] in df.index
    assert remove[0] not in df.index

    assert df.loc[keep[0]]['Id'] != 'new_whale'


def test_duplicate_classes():
    duplicate = DuplicateProcessing()

    duplicate_dict = {
        'Duplicates': ['a b', 'c d', 'e f g'],
        'Verdict': [True, False, True]
    }

    duplicate.df_classes = pd.DataFrame(duplicate_dict)

    df = pd.DataFrame({
        'Image': list('abcdefghijklmnopqrstu'),
        'Id': list('abcdefgabcdefgabcdefg')
    })

    assert len(df) == 21

    df = duplicate.apply(df)

    assert len(df[df['Id'] == 'a']) != 0
    assert len(df[df['Id'] == 'b']) == 0
    assert len(df[df['Id'] == 'c']) != 0
    assert len(df[df['Id'] == 'd']) != 0
    assert len(df[df['Id'] == 'e']) != 0
    assert len(df[df['Id'] == 'f']) == 0
    assert len(df[df['Id'] == 'g']) == 0

    assert len(df) == 21


if __name__ == "__main__":
    test_duplicate_images()
    test_duplicate_classes()
