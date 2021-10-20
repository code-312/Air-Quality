import os
import pandas as pd

os.chdir('../')
CWD = os.getcwd()
DATADIR = os.path.join(CWD, 'data/supplementary')


def import_svi_data():
    """Import Chicago's SVI data for 2018"""
    
    # Import raw CSV files (only FIPS codes from Chicago census tract file)
    csv_svi = os.path.join(DATADIR, 'SVI_2018_Illinois.csv')
    csv_censusTract = os.path.join(DATADIR, 'CensusTracts_2010_Chicago.csv')
    data_svi_il = pd.read_csv(csv_svi)
    censusTracts_chicago = pd.read_csv(csv_censusTract)['GEOID10']
    
    # Select only Chicago census tract SVI data
    data_svi = data_svi_il[data_svi_il['FIPS'].isin(censusTracts_chicago)]
    
    return data_svi


# TODO: import list of Chicago AirNow sensors

if __name__ == "__main__":
    data_svi = import_svi_data()