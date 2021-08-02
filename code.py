import pymysql
import pyexcel

client = pymysql.connect(               
    host = 'localhost',                
    user = 'root',                       
    password = 'Password@123'
)
records = pyexcel.get_records(file_name = "Violence_data.csv")

cursor = client.cursor()

# cursor.execute('CREATE DATABASE Violence') 

cursor.execute('''CREATE TABLE IF NOT EXISTS Violence.dim_country(
    Country VARCHAR(100) PRIMARY KEY
)''')  

cursor.execute('''CREATE TABLE IF NOT EXISTS Violence.dim_gender(
    Gender VARCHAR(100) PRIMARY KEY
)''')  

cursor.execute('''CREATE TABLE IF NOT EXISTS Violence.dim_demographics(
    Demographics_questions VARCHAR(100),
    Demographics_responses VARCHAR(100) PRIMARY KEY
)''')  

cursor.execute('''CREATE TABLE IF NOT EXISTS Violence.dim_year(
    Survey_year DATE PRIMARY KEY
)''')  

cursor.execute('''CREATE TABLE IF NOT EXISTS Violence.fact(
    ID INTEGER(100) AUTO_INCREMENT PRIMARY KEY,
    Country VARCHAR(100),
    Gender VARCHAR(100),
    Demographics VARCHAR(100),
    Year DATE,
    Value VARCHAR(100),
    FOREIGN KEY (Country) REFERENCES Violence.dim_country(Country),
    FOREIGN KEY (Gender) REFERENCES Violence.dim_gender(Gender),
    FOREIGN KEY (Demographics) REFERENCES Violence.dim_demographics(Demographics_responses),
    FOREIGN KEY (Year) REFERENCES Violence.dim_year(Survey_year)
)''')  

for r in records:
    cursor.execute(
    f'''
    INSERT IGNORE INTO Violence.dim_country(Country)
    VALUES (
        "{r['Country']}"
    )
    '''
)

for r in records:
    cursor.execute(
    f'''
    INSERT IGNORE INTO Violence.dim_gender(Gender)
    VALUES (
        "{r['Gender']}"
    )
    '''
)

for r in records:
    cursor.execute(
    f'''
    INSERT IGNORE INTO Violence.dim_demographics(Demographics_questions, Demographics_responses)
    VALUES (
        "{r['Demographics Question']}",
        "{r['Demographics Response']}"
    )
    '''
)

for r in records:
    cursor.execute(
    f'''
    INSERT IGNORE INTO Violence.dim_year(Survey_year)
    VALUES (
        "{(r['Survey Year'])}"
    )
    '''
)

for r in records:
    cursor.execute(
    f'''
    INSERT INTO Violence.fact(Country, Gender, Demographics, Year, Value)
    VALUES (
        "{r['Country']}",
        "{r['Gender']}",
        "{r['Demographics Response']}",
        "{(r['Survey Year'])}",
        "{r['Value']}"
    )
    '''
)

client.commit()