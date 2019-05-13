def map_data(json):

    return {
        "County": json['General']['County'],
        # File No
        "ConsJdgmntFileNum": json['General']['File No'],
        # Checkboxes: In The General Court of Justice
        "District": 'Yes',  # Yes == checked
        "Superior": '',
        # Name and Address of Petitioner
        "NamePetitioner": json['Defendant']['Name'],
        "StreetAddr": '',
        "MailAddr": '',
        "City": "Durham",
        "State": "NC",
        "ZipCode": "27701",
        # Drivers License Number
        "DLNo": '',
        "DLState": '',
        # Race
        "Race": json['Defendant']['Race'],
        # Sex
        "Sex": json['Defendant']['Sex'],
        # Date of Birth
        "DOB": json['Defendant']['Date of Birth/Estimated Age'],
        # Full Social Security Number
        "SNN": '',
        # Age At Time of Offense
        "Age": '',
        # Name and Address of Petitioners Attorney
        "NameAtty": "Arnetta Herring",
        "StAddrAtty": "510 Dillard Street, 6th Fl",
        "MailAddrAtty": "Suite 6400",
        "CityAtty": "Durham",
        "StateAtty": "NC",
        "ZipCodeAtty": "27701",
        }

def f():
    return 'hello'

if __name__=='main':
    with open('test.txt','w') as fi:
        fi.write(f())