LCA Automation Scripts (Part of the Master Thesis by Julius Eberhardt "Towards connected digital product pass using the asset administration shell")

Overview:
    This repository contains a set of Python scripts running on Python 3.11 designed to automate various tasks related to Life Cycle Assessment (LCA) surrounding the Digital Product Passport. The scripts facilitate data processing, setup, and interaction with a server hosting Asset Administration Shells (AAS). The primary functions include uploading JSON data, setting up product and supply chain information, exporting data to CSV, and conductiong updating LCA calculations.

Contents:
    AS_Upload.py: Automates the upload of JSON files containing product, process, procedure, and passport data to a specified server.
    LCA_CSV_Export.py: Exports the carbon footprint data from the server into a CSV file.
    LCA_Product_Setup.py: Sets up product information in the openLCA software by creating flows and processes based on data retrieved from the server.
    LCA_SupplyChain_Setup.py: Configures the supply chain information for products, including setting up flows and processes in openLCA based on Bill of Materials (BOM) data.
    LCA_Update.py: Updates the energy and transport flows for products and performs LCA calculations, updating the results back to the server.
    Method_Toolbox.py: Provides utility functions used across other scripts, including functions for retrieving and updating JSON data from the server.
    Middleware_Startup.py: Initializes a middleware server to handle REST API interactions for the product, process, procedure, and passport models.

Requirements:
    Ensure you have the following dependencies installed using pip
    - AAS2OpenAPI 
    - pandas
    - olca-ipc
    - openpyxl

    Also, please download the openLCA Desktop Client and import the PET Case study database, which can be downloaded here: https://nexus.openlca.org/downloads

    Importing the Database is explained in this Tutorial: https://youtu.be/8-RU_XOCCaI?si=9fdMR_k-XVSUNwKY 


Getting Started:
    To start the overall script, first make sure you have the dependencies abouve installed. Next, make sure that you have have started the AAS2OpenAPI Server in Docker. If this is your first time using the AAS2OpenAPI, use the repository of the AAS2OpenAPI to gather the relevant dockerfile. The command 

    docker-compose -f dockercompose-dev.yaml up

    should also work within this repo to set up the inital servers for the script to work. Execute this in your terminal.

    Next, set up the middleware by executing the "Middleware_Startup.py" file. This enables the server to have the required information about our AASs. Note: If you want to experiment with other model structures or change the names, make sure to adjust these within the subsequent pyhton file, otherwise the middleware will not be able to handle your uploads.

    After setting up the middleware, you can upload your examplary administration shells. These must match the provided class structures and are specified as JSON files under Input_Files. By executing the AAS_Upload.py, the files are provided on the server and can be accessed using HTML commands. This will probalby take up to a minute. It is important that general principles (such as the passport ID within product matching the ID of the actual passport) are followed.

    After uploading all the AASs, you must start the IPC Server within openLCA. To do this, open your database, select developer tools and then IPC server and start up the server under the port 8083. Note: This port is necessary as it is fixed within the scripts and could otherwise create conflict with the middleware servers. Please make sure that the provided category specified within the LCA_Product_Setup.py (should be named "Stellmotor_Skript") exist both within the flows as well as processes within the openLCA database. By default, you dont have to do anything in the repo, only in openLCA, this is only important should you wish to adapt the example to another use case. The naming of the category is not important for the funciton of openLCA. Also make sure that your product_id set to the value of your main product shell (not the passport ID!) so that the correct information is pulled from the server. Your product should contain an id_short and id for the script to work.

    After setting up the production environment, the LCA of the product and overall product system can be calculated. For this, you must execute the LCA_Update.py file. Make sure that:
        - The necessary auxillary excel is present at your chosen file path (ýou should be able to copy the file path from your editor, as the examplary excel is present within the repo)
        - Your ID is set within the script
    This should add the overal footprint to your desired passport. The saved info could also be used to save it somewhere else, i.e. an Excel sheet or within the SDM-Shells

    After the calculation has been done, you may export your data for the carbon footprint using the LCA_CSAV_Export.py file. The created csv can be used for examample by PowerBI to create a sankey chart. The CSV export chart can also be modified to grab any datapoints from the uploaded AASs using Get requests.

    Congrats! You have conducted the initial implementation of the script. To start again, shut down the Middleware server and follow the steps above again

Notes:
    - The LCA_SupplyChain_Setup.py is a legacy file to create the necessary Background for the product system. If desired, you may use it to build the overall product system within openLCA. Note that the script only creates processes and flows but does not link them.
    - Currently, the middleware will do funky things to the id_short fields and description fields. These are therefore not included in any of the scripts in a productive manner. Future versions of the middleware will negate this problem.
    - The AASs of the product components (not the Passports) also include GHG components. These were not used as the used database in openLCA is not able to calculate Scope 1-3 emissions.