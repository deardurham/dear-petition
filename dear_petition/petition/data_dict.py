def map_data(json):

    return {
        "County": json.get('General',{}).get('County',''),
        # File No
        "ConsJdgmntFileNum": json.get('General',{}).get('File No',''),
        # Checkboxes: In The General Court of Justice
        "District": json.get('General', {}).get('District',''),
        "Superior": json.get('General', {}).get('Superior',''),
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
        "NameAtty": json.get('NameAtty', ''),
        "StAddrAtty": json.get('StAddrAtty', ''),
        "MailAddrAtty": json.get('MailAddrAtty', ''),
        "CityAtty": json.get('CityAtty', ''),
        "StateAtty": json.get('StateAtty', ''),
        "ZipCodeAtty": json.get('ZipCodeAtty', ''),
        # Agency 1
        "NameAgency1": json.get('NameAgency1', ''),
        "AddrAgency1": json.get('AddrAgency1', ''),
        "MailAgency1": json.get('MailAgency1', ''),
        "CityAgency1": json.get('CityAgency1', ''),
        "StateAgency1": json.get('StateAgency1', ''),
        "ZipAgency1": json.get('ZipAgency1', ''),
        # Agency 2
        "NameAgency2": json.get('NameAgency2', ''),
        "AddrAgency2": json.get('AddrAgency2', ''),
        "MailAgency2": json.get('MailAgency2', ''),
        "CityAgency2": json.get('CityAgency2', ''),
        "StateAgency2": json.get('StateAgency2', ''),
        "ZipAgency2": json.get('ZipAgency2', ''),
        }
