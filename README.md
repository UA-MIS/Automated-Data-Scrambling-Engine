# Automated-Data-Scrambling-Engine
This project was created by a University of Alabama MIS Capstone Team (Maddie Little, Kevin Mohrmann, Sydney Bonner, Will Fischer, and Noah Coffin)

The Automated Data Scrambling Engine or ADSE, is a python application that is used to mask and generate data related to personally identifiable information (PII). The application seeks to reduce the time it takes for PwC to scramble PII from their clients and upload this information back into their Oracle cloud. The ADSE works with a number of different PII including social security numbers, addresses, email addresses, names, and several more. The application ingests a flat file type (csv or dat for example) and scrambles the data to protect sensitive client data. ADSE utilizes a number of packages:
TkInter: Serves as a graphical user interface (GUI) .
Pandas: Places information into data frames and allows for easy manipulation of data.
Faker: Built-in methods allows for easy creation of serveral different forms of fake data. 

The ADSE scrambles the client data then gives the option to export the file as a pipe delimited dat file which can then be zipped. 

Utilzing auto-py-to-exe, we have turned the application into an executable for ease of use by PwC and their clients.
The implementation of the ADSE will allow PwC and their clients to easily scramble their sentitive data in a timely manner.  