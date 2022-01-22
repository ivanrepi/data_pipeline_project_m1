# Where is my bike?

Given a place of interest in Madrid, the application will return the nearest BiciMad station as well as walking directions to reach it.

![Image](https://www.cnet.com/a/img/18OAz996_EOEv_30SBWrw99jBoA=/2018/03/23/691b3998-080c-4a8c-aa68-575ff95c1b55/pile-of-bikes.jpg)

---
## **Description**
The app contains 2 types of user, the admin one and the final user one.

- The **administrator** role (with an authentication double step) will be in charge of uploading the information for the user, as well as access to the different APIs with their own credentials.
- The **final user** role will be able to chose, if he/she wants to get a table with all 'Places of Interest' of Madrid's city, or conversely he/she wants to receive the nearest station for an specific 'Place of Interest'.

---
## **Getting Started**
### :baby: **Status**
This is part of Ironhack Data Analytics Bootcamp. The main goal is to build a complete pipeline app.

### :computer: **Dependencies**

- This repository is tested on **Python 3.7+**.
- Create a virtual environment with the version of Python you're going to use and activate it.

- Install [pandas](https://pandas.pydata.org/docs/user_guide/index.html) library. Copy and paste next command in your master branch:
    ```
    conda install pandas
    ```
- Install [geopandas](https://geopandas.org/en/stable/) library. Copy and paste next command in your master branch:
    ```
    conda install -c conda-forge geopandas
    ```
- Install [requests](https://docs.python-requests.org/en/latest/) library. Copy and paste next command in your master branch:
    ```
    python -m pip install requests
    ```
- Install [dotenv](https://pypi.org/project/python-dotenv/) library. Copy and paste next command in your master branch:
    ```
    pip install python-dotenv
    ```
- Install [pretty-html-table](https://pypi.org/project/pretty-html-table/) library. Copy and paste next command in your master branch:
    ```
    pip install pretty-html-table
    ```
- Install [fuzzywuzzy](https://pypi.org/project/pretty-html-table/) library. Copy and paste next command in your master branch:
    ```
    pip install fuzzywuzzy
    ```
- Be sure next Python modules are installed: [sys](https://docs.python.org/3/library/sys.html) , [os](https://docs.python.org/3/library/os.html), [smtplib](https://docs.python.org/3/library/smtplib.html), [email.mime](https://docs.python.org/3/library/email.mime.html), [random](https://docs.python.org/3/library/random.html), [warnings](https://docs.python.org/3/library/warnings.html), [webbrowser](https://docs.python.org/es/3/library/webbrowser.html).

&nbsp;

---
## :lock: **ADMIN ROLE**

### :clipboard: **Overview**
Admin role should chose what kind of 'Place of Interest' the user will use. It can be obtained [here](https://datos.madrid.es/nuevoMadrid/swagger-ui-master-2.2.10/dist/index.html?url=/egobfiles/api.datos.madrid.es.json#/).

The app includes a double authentication step. Admin will receive a security number in his/her email, to verify his/her identity.


### :wrench: **Installing**
Once all dependencies are clear, follow the next steps to install it:
1. Clone this [repo](https://github.com/ivanrepi/nearest_bicimad_station)
2. Create an account on EMT Madrid developer website ([here](https://mobilitylabs.emtmadrid.es/es/doc/new-app))
3. In your local repository, create the file ".env", with the next parameters:
    ```
    path="path of the repo"

    sender_email = "type your email" 
    password_sender = "type your email password"
    admin_email="type admin email" #For double auth. Can be different of the sender one
    emt_madrid_email="email from step 2"
    emt_madrid_pwd="password from step 2"
    ```
4. Open the main_admin.py file, and edit the URL of the 'Place of Interest'. By default, it is settled "Instalaciones Deportivas Básicas de Madrid".

### :point_right: **Executing program**
1. Open the terminal.
2. Look for the main_admin.py file in your repo.
3. Execute the next command:
    ```
    python main_admin.py
    ```
4. It will ask you for an admin email. It should be the same settled in ".env" file.
5. If email address is correct, admin should receive a security code in his/her email.
6. Type this code in the terminal and press enter.
7. If code is correct, it starts the process to prepare the result table (which one that user will work with).

### :boom: **Core technical concepts and inspiration**
The main goal of this role is to work with double authentication mode, as well as divide the app in two kind of users. 
Working with this division, final user will not have to wait for data preparation (as this is part of the admin work)

&nbsp;


## **USER ROLE**

### :clipboard: **Overview**
User role should chose if wants to get the complete table of 'Places of Interest' of Madrid with its nearest Bicimad station, or contrary wants to know the nearest BiciMad station for an specific 'Place of Interest'.

The app includes an advance searcher, which is able to find the result even it has not been written correctly.
If it finds more than one similar result, it shows user all the results found.

### :wrench: **Installing**
Once all dependencies are clear, follow the next steps to install it:
1. Clone this [repo](https://github.com/ivanrepi/nearest_bicimad_station)
2. In your local repository, create or edit the file ".env", with the next parameters:
    ```
    path="path of the repo"
    ```

### :point_right: **Executing program**
1. Open the terminal.
2. Look for the main_user.py file in your repo.
3. Execute the next command to get the list of possible arguments to run the app:
    ```
    python main_user.py -h
    ```
-  Run next command to get the complete table of all "Places of Interest" with its nearest BiciMad station:
    ```
    python main_user.py -i 1
    ```
- Run next command to get the nearest BiciMad station for an specific "Place of Interest":

    ```
    python main_user.py -i 2
    ```
    - Enter the 'Place of Interest' you are interested in and press Enter.
    - Get the nearest BiciMad station with its location.
    - Get the number of available bikes in that moment.
    - Press enter to obtain the walking instructions to arrive until the station (Google Maps).


### :boom: **Core technical concepts and inspiration**
It has been developed with an argparse function, which helps the user to chose, before opening the app, to decide how want to get the results.

It includes also fuzzywuzzy library, working as an advanced searcher. It helps the user to find the result even it is written wrongly.

Finally, thanks to EMT Madrid API, user can obtain in real time, the number of available bikes in that nearest station.

&nbsp;

---

### :file_folder: **Folder structure**
```
└── project
    ├── __trash__
    │ 
    ├── .git
    │ 
    ├── .gitignore
    │ 
    ├── nearest_bicimad_station.html
    │ 
    ├── README.md
    │ 
    ├── main_user.py
    │ 
    ├── main_admin.py
    │ 
    ├── modules
    │   └── geo_calculations.py
    │ 
    ├── p_acquisition
    │   └── acquisition.py
    │
    ├── p_wrangling
    │   └── wrangling.py
    │
    ├── p_analysis
    │   └── analysis.py
    │
    ├── p_reporting
    │   └── reporting.py
    │
    └── data
        ├── raw
        ├── processed
        └── results
```

> Do not forget to include `__trash__` and `.env` in `.gitignore` 

&nbsp;
### :shit: **ToDo**
:black_square_button: Create an API to connect to Places of Interests webstite.  
:black_square_button: Get all places of interest at the same time, and not have to settled it in the main_admin script.  
:black_square_button: Add possibility to go by car, walking or taxi to the nearest BiciMad station.  
:black_square_button: Create the UI to help the final user to use it.  

---


