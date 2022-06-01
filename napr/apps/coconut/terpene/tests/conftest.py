"""Sharing fixtures across multiple files."""

import pandas as pd

from sklearn.model_selection import train_test_split

import pytest

from napr.utils.random import (
    rand_list_int,
    rand_list_float,
    rand_list_choices,
    rand_list_string,
)


@pytest.fixture(scope="module")
def data():
    """The data for the tests."""
    chemicalSubClass_21_3 = [
        "Diterpenoids",
        "Cholestane steroids",
        "Terpene glycosides",
        "Triterpenoids",
        "Sesquiterpenoids",
        "Monoterpenoids",
        "Eicosanoids",
        "Pregnane steroids",
        "Terpene lactones",
        "Steroidal glycosides",
        "Phosphosphingolipids",
        "Ergostane steroids",
        None,
        "Steroid esters",
        "Fatty acids and conjugates",
        "Steroid lactones",
        "Sesterterpenoids",
        "Fatty acyl glycosides",
        "Glycerophosphoethanolamines",
        "Gorgostanes and derivatives",
        "Fatty alcohols",
        "Fatty amides",
        "Fatty acyl thioesters",
        "Tetraterpenoids",
        "Oxosteroids",
        "Monoradylglycerols",
        "Steroidal alkaloids",
        "Diradylglycerols",
        "Cucurbitacins",
        "Glycerophosphocholines",
        "Glycosphingolipids",
        "Fatty acid esters",
        "Stigmastanes and derivatives",
        "Quinone and hydroquinone lipids",
        "Glycerophosphoglycerophosphoglycerols",
        "Cycloartanols and derivatives",
        "Bile acids, alcohols and derivatives",
        "Glycerol vinyl ethers",
        "Glycerophosphoinositols",
        "Steroid acids",
        "Hydroxysteroids",
        "Fatty aldehydes",
        "Lineolic acids and derivatives",
        "Triradylcglycerols",
        "Fatty alcohol esters",
        "Glycerophosphoserines",
        "Hopanoids",
        "Glycerophosphoglycerols",
        "Androstane steroids",
        "Polyprenols",
        "Glycosylglycerols",
        "Estrane steroids",
        "Sesquaterpenoids",
        "Delta-7-steroids",
        "Glycerophosphoinositol phosphates",
        "17-furanylsteroids and derivatives",
        "Ecdysteroids",
        "Furostanes and derivatives",
        "Glycerophosphoglycerophosphates",
        "Ceramides",
        "Vitamin D and derivatives",
        "Azasteroids and derivatives",
        "Retinoids",
        "Sulfated steroids",
        "Furospirostanes and derivatives",
        "Physalins and derivatives",
        "Acyltrehaloses",
        "Polyterpenoids",
        "Delta-5-steroids",
        "Glycerophosphates",
        "Isoprenoid phosphates",
        "5,6-epoxysteroids",
        "CDP-glycerols",
        "C24-propyl sterols and derivatives",
        "Polyprenylphenols",
        "Glycerol ethers",
        "Oxasteroids and derivatives",
        "Lysobisphosphatidic acids",
        "Semilysobisphosphatidic acids",
        "Glycerophosphonoethanolamines",
        "Halogenated steroids",
        "Glycero-3-pyrophosphates",
        "Phosphonosphingolipids",
        "Delta-1,4-steroids",
        "Glycerophosphonocholines",
    ]
    size = len(chemicalSubClass_21_3)

    def _rand_bcutDescriptor():
        """Generate a list of random bcutDescriptor."""
        result = []
        for _ in range(size):
            rand_list = rand_list_int(size=6)
            result.append("[" + ",".join(map(str, rand_list)) + "]")
        return result

    def _rand_textTaxa():
        """Generate a list of random textTaxa."""
        return rand_list_choices(
            elements=["plants", "marine", "bacteria", "fungi"], size=size
        )

    data = {"chemicalSubClass": chemicalSubClass_21_3}
    for column in [
        "molecular_weight",
        "alogp",
        "npl_score",
        "lipinskiRuleOf5Failures",
        "hBondAcceptorCount",
        "hBondDonorCount",
    ]:
        data[column] = rand_list_float(size=size)
    data["bcutDescriptor"] = _rand_bcutDescriptor()
    data["textTaxa"] = _rand_textTaxa()
    data["directParentClassification"] = rand_list_string(len_str=5, size=size)
    return pd.DataFrame(data)


@pytest.fixture(scope="module")
def dropped_columns():
    """The columns to drop."""
    return ["molecular_weight", "bcutDescriptor", "textTaxa"]


@pytest.fixture(scope="module")
def train_test_data(data, dropped_columns):
    """The training and testing data."""
    data_clean = data.drop(dropped_columns, axis=1, inplace=False)
    train_data, test_data = train_test_split(
        data_clean, test_size=0.25, random_state=777
    )
    return train_data, test_data
