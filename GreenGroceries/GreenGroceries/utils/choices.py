import os
import pandas as pd

LANGUAGES_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'languages.csv')
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'categories.csv')
COUNTRIES_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'countries.csv')


def get_label_name(string):
    return string.replace("_", " ").capitalize()


class ModelChoices:
    def __init__(self, choices_list):
        for item in choices_list:
            setattr(self, item.lower(), get_label_name(item))

    def choices(self):
        return [(k, v) for k, v in self.__dict__.items()]

    def values(self):
        return [v for v in self.__dict__.keys()]

    def labels(self):
        return [l for l in self.__dict__.values()]


df_languages = pd.read_csv(LANGUAGES_PATH, sep=',')
df_categories = pd.read_csv(CATEGORIES_PATH, sep=',')
df_countries = pd.read_csv(COUNTRIES_PATH, sep=',')

LanguageChoices = ModelChoices(df_languages.language.unique())
WordCategoryChoices = ModelChoices(df_categories.category.unique())
CountryChoices = ModelChoices(df_countries.country.unique())
