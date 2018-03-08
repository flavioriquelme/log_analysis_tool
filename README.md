# Log Analysis Tool

Log Analysis Tool Project (python, postgreSQL) for Udacity Full Stack Nanodegree

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Have the Oracle VM Virtualbox installed
```
https://www.virtualbox.org/wiki/Downloads
```

Have the Vagrant installed
```
https://www.vagrantup.com/downloads.html
```

### Installing

Download the Vagrant VM config files provided by Udacity Full Stack Nanodegree course:
```
git clone https://github.com/udacity/fullstack-nanodegree-vm.git
```

Bring the VM up with Vagrant, by running the following command from the path where the Vagrant VM config file downloaded in the previous step is located:
```
vagrant up
```

Download the SQL script to create and populate a DB named "news":
```
https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
```

Execute the DB creation script just downloaded:
```
psql -d news -f newsdata.sql
```

Create views in PSQL required by the Log Analysis Tool:
```
CREATE VIEW DATE_VIEWS AS
SELECT to_char(time, 'DD-Mon-YYYY') as DATE, count(*) as VIEWS
 FROM log
GROUP BY DATE
ORDER BY DATE;

CREATE VIEW DATE_ERRORS AS
SELECT to_char(time, 'DD-Mon-YYYY') as DATE, count(*) as ERRORS
 FROM log
WHERE status !='200 OK'
GROUP BY DATE
ORDER BY DATE;
```

### Running the tool

To run the Log Analysis tool:
```
python loganalysis.py
```

An output report will be available in the same path of loganalysis.py, named as:
```
log_analysis_report_<YYYY-MM-DD>
```

## Author

**Flavio Fernandez** - (https://github.com/flavioriquelme)
