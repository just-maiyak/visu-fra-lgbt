from typing import Dict
import numpy as np
import pandas as pd
import pycountry
import flag
from os.path import join

countries = {c.name: c.alpha_2 for c in pycountry.countries}
c_names = {c.alpha_2: c.name for c in pycountry.countries}

groups = ["Gay men", "Lesbian women", "Bisexual women", "Bisexual men", "Transgender"]


def open_data(path: str = "data") -> Dict[str, pd.DataFrame]:
    pre_path = lambda f: join(path, f)
    return {
        "daily_life": clean_data(pd.read_csv(pre_path("LGBT_Survey_DailyLife.csv"))),
        "rights_aware": clean_data(
            pd.read_csv(pre_path("LGBT_Survey_RightsAwareness.csv"))
        ),
        "trans_questions": clean_data(
            pd.read_csv(pre_path("LGBT_Survey_TransgenderSpecificQuestions.csv"))
        ),
        "discrimination": clean_data(
            pd.read_csv(pre_path("LGBT_Survey_Discrimination.csv"))
        ),
        "violence": clean_data(
            pd.read_csv(pre_path("LGBT_Survey_ViolenceAndHarassment.csv"))
        ),
        "counts": counts(path),
    }


def counts(path: str = "data"):
    pre_path = lambda f: join(path, f)
    counts = pd.read_csv(pre_path("LGBT_Survey_SubsetSize.csv"))
    country_counts = counts.iloc[1:].sort_values("N", ascending=False)
    country_counts["CountryName"] = country_counts.CountryID.apply(c_names.get)
    return country_counts


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df.rename(columns={"CountryCode": "CountryName"}, inplace=True)
    codes = [countries.get(country, "Unknown code") for country in df["CountryName"]]
    df["CountryID"] = codes
    df.loc[df["CountryName"] == "Czech Republic", "CountryID"] = "CZ"
    df["CountryFlag"] = df["CountryID"].apply(lambda x: x + flag.flagize(":" + x + ":"))
    df.loc[df["notes"] == " [1] ", "notes"] = "[1]"
    df.loc[df["notes"] == "[1]", "percentage"] = np.NaN
    df["percentage"] = df["percentage"].astype("float")
    return df
