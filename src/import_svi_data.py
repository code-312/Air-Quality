import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

CWD = os.getcwd() # Assuming run from root
DATADIR = os.path.join(CWD, 'data/supplementary')
CRS = 'EPSG:3857'

# Define subset of variables to look into
# Prepend 'E' for estimates, 'M' for margins of error
# Then, if not absolute numbers, prepend 'P' for percentage, 'PL' for percentile (within IL, not Chicago!)
# If not a binary category, E = EP generally, but see documentation for details
# Or, prepend F to flag values in the 90th percentile (again, within IL, not Chicago!)
SVIVARS = {'TOTPOP': "Population",
           'HH': "Households",
           'POV': "Persons below poverty",
           'UNEMP': "Civillian (age 16+) unemployed",
           'PCI': "Per capita income",
           'MINRTY': "Minority (all persons except white, non-Hispanic)",
           'NOVEH': "Households with no vehicle available",
           }

SVITHEMES = {'RPL_THEME1': "Percentile ranking for Socioeconomic theme",
             'RPL_THEME2': "Percentile ranking for Household Composition theme",
             'RPL_THEME3': "Percentile ranking for Minority Status/Language theme",
             'RPL_THEME4': "Percentile ranking for Housing Type/Transportation theme",
             'RPL_THEMES': "Overall percentile ranking",
             }

def import_svi_data():
    """Import Chicago's SVI data for 2018"""
    
    # Import FIPS codes from Chicago census tract file
    csv_censusTract = os.path.join(DATADIR, 'CensusTracts_2010_Chicago.csv')
    chicagoFIPS = pd.read_csv(csv_censusTract)['GEOID10']
    
    # Import SVI shapefile as GeoDataFrame
    f_shp = os.path.join(DATADIR, "SVI_2018_ILLINOIS_tract/SVI2018_ILLINOIS_tract.shp")
    gdf = gpd.read_file(f_shp).to_crs(CRS) # Original is epsg:4269
    gdf.replace(-999, np.nan, inplace=True)
    gdf['FIPS'] = gdf['FIPS'].astype(int)
    
    # Select Chicago data only
    gdf = gdf.loc[gdf['FIPS'].isin(chicagoFIPS)]
    
    # Plot a key metric for confirmation
    gdf.plot(column='RPL_THEMES',
             legend=True,
             legend_kwds={'label': "Overall Social Vulnerability Index Theme Percentile Ranking"})
    plt.savefig('figures/census_tracts_chicago.png', bbox_inches='tight', dpi=600)
    
    return gdf


if __name__ == "__main__":
    data = import_svi_data()