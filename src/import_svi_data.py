import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

os.chdir('../')
CWD = os.getcwd()
DATADIR = os.path.join(CWD, 'data/supplementary')


def import_svi_data():
    """Import Chicago's SVI data for 2018"""
    
    # Import FIPS codes from Chicago census tract file
    csv_censusTract = os.path.join(DATADIR, 'CensusTracts_2010_Chicago.csv')
    chicagoFIPS = pd.read_csv(csv_censusTract)['GEOID10']
    
    # Import SVI shapefile
    shp = os.path.join(DATADIR, "SVI_2018_ILLINOIS_tract/SVI2018_ILLINOIS_tract.shp")
    data_shp_il = gpd.read_file(shp)
    data_shp_il['FIPS'] = data_shp_il['FIPS'].astype(int)
    
    # Select Chicago data only
    data_shp = data_shp_il.loc[data_shp_il['FIPS'].isin(chicagoFIPS)]
    
    # Plot geographic data for confirmation
    data_shp.plot()
    plt.savefig('figures/census_tracts_chicago.png', bbox_inches='tight', dpi=300)
    
    return data_shp


# TODO: import list of Chicago AirNow sensors


if __name__ == "__main__":
    data = import_svi_data()