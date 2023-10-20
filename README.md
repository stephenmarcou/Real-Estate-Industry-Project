[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/SGWUF1eE)


# MAST30034 Generic Real Estate Consulting Project README.md

- Names: `Liam Bindokas`,  `Cherry Xu`, `Jaden Ling`, `Seamus Staite`, `Stephen Marcou`


**Research Goal:** To create models that have the ability to predict growth in rental properties in Victoria, as well as identify most affordable and most liveable postcodes in  Victoria


To run the pipeline, please visit the `scripts` directory 

Go to the `property_data_scripts` directory then run the files in order:
   
1.  `scrapev2.py`: This scrapes all the victorian property data from the domain site saving the dataframe into the `data/landing` directory.
2.  `preprocessing_property_data.py`: this preprocesses the property data saving the preprocessed data into the `data/raw` directory.
3.  `curate_property_data.py`: this curates the property data saving the curated data into the `data/curated` directory.
go to the `crime_data_scripts` directory and run the files in the following order:
4.  `crime_data_dowmload.py`: this downloads the crime statistics for Victoria and 
5. `crime_data_preprocess.py`: this preprocesses the crime data saving it into the `data/raw` directory.

6. `postcode_shapefile_download.py`: downloads the postcode shapefiles used for the folium maps and saves into the `data/curated` directory. 
7. `SA2_shapefile_download.py`: downloads the SA2 shapefiles and postcode_to_SA2 excel file and saves into the `data/landing` directory.
8. `shapefile_preprocess.py`: preprocesses the SA2 shapefile to geojson and converts postcode_to_SA2 excel file to csv and saves into respectively the `data/curated/geojson` directory and `data/curated/sa2_to_postcode` directory.
9.  `school_data_download.py`: downloads all victorian school location data and scrapes the 150 top VCE schools saving the data into `data/landing/school_data` 
10. Manually download all victorian university locations from https://adp-access.aurin.org.au/dataset/aurin-aurin-national-education-dataset-universities-2018-na. Use Unimelb account to log in and save the csv into `data/landing/school_data`

11. `type_of_towns_scripts/type_of_town.py`: downloads all data to do with towns and their promixity in Victoria
12. `type_of_towns_scripts/preprocess_all_towns.py`: preprocesses the town, postcode and lat and long data such that one file is created, `data/raw/all_town_data.csv`
13. Manually download all supermarket locations from https://www.yellowpages.com.au/vic/supermarkets-grocery-stores-20613-category-a1. Enter data into `data/landing/supermarket_raw_data.csv`
14. Manually download all PTV data from https://datashare.maps.vic.gov.au/search?q=uuid%3D1792cbe0-25e5-52a0-8bc2-cc2294051634
Enter data into 'data/landing/ptv_data'
15. Manually download postcode polygon data from https://datashare.maps.vic.gov.au/search?q=uuid%3D46bba391-0d67-5bd7-b0bb-bb37945c5c4a
Enter data into 'data/landing/postcode_polygon_data'

17. `school_data_preprocessing_raw.py`: preprocesses school and university data and saves into `data/raw/school_data`
18. `school_data_preprocessing_curated.py`: curates the school and university data and saves into `data/curated/school_data`
19. `hospital_data_download.py`: downloads the hospital data and saves into `data/landing/hospital_data`
20. `hospital_data_raw_preprocessing.py`: preprocess the hospital data and saves into `data/raw/hospital_data`
21. `hospital_data_raw_preprocessing.py`: curates the hospital data (including retrieving coordinates for the locations) saves into `data/curated/hospital_data`
22. `ptv_data_preprocess_raw.py`: preprocesses PTV data and saves into `data/raw/ptv`

23. `type_of_towns_scripts/create_town_dataframe.py`: curates all the town data and saves it in a clean dataframe in `data/curated`
24. `supermarket_scripts/supermarket_curate.py`: curates the supermarket data into a dataframe saved into `data/curated`


25. `download_sa2_info.py`: downloads all the data for each SA2 district and saved into `data/landing/suburb_info`, this script relies on `SA2_shapefile_download.py` being ran first

26. `postcode_shapefile_download.py`: downloads the postcode shapefiles and saves into the `data/landing` directory.
27. `preprocess_sa2_info.py`: Gathers all the important information from each SA2 district from each census year since 2011,
and saves the each year's info into the `data/curated` directory

#### Put in all of your scripts you run to get the data


#### run the scripts or notebooks that merge all the data into a single dataframe.

1. `trial_projection.ipynb`: this notebook uses the average growth rate between census data to predict the census data for 2026 for each SA2 district, and outputs it to `data/curated` folder as `suburb_info_2026.csv`
2. `rental_sa2.ipynb`: this notebook adds the SA2 district and shapefile geometry attribute to each property in the form of `data/curated/rental_data_sf.csv` as well as changes the SA2 data to postcode based data. 
3. `distance_school_houses.ipynb`: this notebook calculates the distance from all properties to closest primary and secondary school, and also to closest university campus. It merges these distance metrics with the property data and is saved into `data/curated/rental_data_distance_uni_school_sf.csv`
4. `distance_hospital_houses.ipynb`: this notebook calculates the distance from all properties to closest hospital. It merges this distance metric with the output csv from last step and is saved into `data/curated/rental_data_distance_sf.csv`
5. `merge_supermarket_and_town_data.py`: the python script merges the data from the supermarket dataframe and the town dataframe with the rental data and saves it into `data/curated/rental_data_town_join.csv`
6. `merge_rental_data.ipynb`: this notebook merges all features (both internal and external) to a single dataframe and saves into `data/curated/merged_data.csv`
7. 'distance_ptv.ipynb': this notebook calculates the distance from all properties to the closest train station. It merges the distance metric with the property data and is saved into 'data/curated/rental_data_train_station.csv'
   

number. `join_crime_realestate.ipynb`: this notebook will join the crime data with the property data, saving the data to `data/curated` directory.

Having run all the scripts to download the data we move to analyse the data
Visit the `notebooks` directory, run the following notebooks to perform the evaluation of the datasets.

1. `affordability.ipynb`: runs the affordability model on the dataset outputing the most affordable suburbs into `data/curated` directory.
2. `liveability_analysis.ipynb`: this notebook runs the liveability models on the datasets, creating many rankings and geospatial plots that are used in the presentation.
3. `dist_cc_geo.ipynb`: this notebook creates some visualisations to do with city centres, in order to help us determine if we are on the right track
4. `q1_modelling.ipynb`: this notebook runs and anlayses the XGBoost model that predicts rent prices. It identifies the most important features to predict rent prices. It saves the csv file used for modelling into `data/curated/data_XGBoost_before_onehotencode.csv`. The most important features are saved into `data/curated/top_features.csv` 
5. `income_school_geospatial.ipynb`: this notebook creates folium map of the average household income of SA2 areas combined with markers of the top 150 VCE schools. The map is saved into the `plots/income_school_geo.html`
6. `property_school_geo.ipynb`: this notebook creates two folium maps, one for the log average rental price per bed for houses in SA2 areas combined with markers of the top 150 VCE schools and the other one for the log average rental price per bed for apartment units in SA2 areas combined with markers of the top 150 VCE schools. The resepective maps are saved into the `plots/school_house_rentprice_map.html` and `plots/school_unit_rentprice_map.html`
7. `trial_growth_rate.ipynb`: this notebook is intended for use to show the general linear trend in growth rates between 2011 and 2021 in census data
8. `open_space.ipynb`: this notebook finds the distance to the closest park for each rental property and outputs the result to `data/curated` folder as `rental_data_closest_park.csv`
9. `q2_modelling.ipynb`: this notebook used the XGBoost model created in `q1_modelling.ipynb` to predict the rental prices in 2026 and calculated the growth rate between the years.
10. `predictions_geospatial.ipynb`: this notebook creates the map of the postcodes' growth rates that was calculated in `q2_modelling.ipynb`.

With all the predictions and models ran, navigate to `notebooks/summary_notebook.ipynb`
It contains a summary and evaluates the models created to address the research goal.
