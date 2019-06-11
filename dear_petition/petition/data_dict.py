def map_data(json):

    return {
        "County": json.get('General',{}).get('County',''),
        # File No
        "ConsJdgmntFileNum": json.get('General',{}).get('File No',''),
        # Checkboxes: In The General Court of Justice
        "District": 'Yes',  # Yes == checked
        "Superior": '',
        # Name and Address of Petitioner
        "NamePetitioner": json.get('Defendant',{}).get('Name',''),
        "StreetAddr": '',
        "MailAddr": '',
        "City": "Durham",
        "State": "NC",
        "ZipCode": "27701",
        # Drivers License Number
        "DLNo": '',
        "DLState": '',
        # Race
        "Race": json.get('Defendant',{}).get('Race',''),
        # Sex
        "Sex": json.get('Defendant',{}).get('Sex',''),
        # Date of Birth
        "DOB": json.get('Defendant',{}).get('Date of Birth/Estimated Age',''),
        # Full Social Security Number
        "SNN": '',
        # Age At Time of Offense
        "Age": '',
        # Name and Address of Petitioners Attorney
        "NameAtty": "",
        "StAddrAtty": "",
        "MailAddrAtty": "",
        "CityAtty": "",
        "StateAtty": "",
        "ZipCodeAtty": "",
        }