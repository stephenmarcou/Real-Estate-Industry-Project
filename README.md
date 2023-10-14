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


##### Put in all of your scripts you run to get the data


##### run the scripts or notebooks that merge all the data into a single dataframe.

number. `join_crime_realestate.ipynb`: this notebook will join the crime data with the property data, saving the data to `data/curated` directory.



Having run all the scripts to download the data we move to analyse the data
Visit the `notebooks` directory, run the following notebooks to perform the evaluation of the datasets.

number. `affordability.ipynb`: runs the affordability model on the dataset outputing the most affordable suburbs into `data/curated` directory.





With all the predictions and models ran, navigate to `notebooks/summary_notebook.ipynb`
It contains a summary and evaluates the models created to address the research goal.

