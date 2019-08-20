def map_data(json):

    data = {
        "County": {"V": json.get("General", {}).get("County", "")},
        # File No
        "ConsJdgmntFileNum": {"V": json.get("General", {}).get("File No", "")},
        # Checkboxes: In The General Court of Justice
        "District": {"AS": json.get("General", {}).get("District", "")},
        "Superior": {"AS": json.get("General", {}).get("Superior", "")},
        # Name and Address of Petitioner
        "NamePetitioner": {"V": json.get("Defendant", {}).get("Name", "")},
        "StreetAddr": {"V": ""},
        "MailAddr": {"V": ""},
        "City": {"V": "Durham"},
        "State": {"V": "NC"},
        "ZipCode": {"V": "27701"},
        # Drivers License Number
        "DLNo": {"V": ""},
        "DLState": {"V": ""},
        # Race
        "Race": {"V": json.get("Defendant", {}).get("Race", "")},
        # Sex
        "Sex": {"V": json.get("Defendant", {}).get("Sex", "")},
        # Date of Birth
        "DOB": {"V": json.get("Defendant", {}).get("Date of Birth/Estimated Age", "")},
        # Full Social Security Number
        "SNN": {"V": ""},
        # Age At Time of Offense
        "Age": {"V": ""},
        # Name and Address of Petitioners Attorney
        "NameAtty": {"V": json.get("NameAtty", "")},
        "StAddrAtty": {"V": json.get("StAddrAtty", "")},
        "MailAddrAtty": {"V": json.get("MailAddrAtty", "")},
        "CityAtty": {"V": json.get("CityAtty", "")},
        "StateAtty": {"V": json.get("StateAtty", "")},
        "ZipCodeAtty": {"V": json.get("ZipCodeAtty", "")},
        # Agency 1
        "NameAgency1": {"V": json.get("NameAgency1", "")},
        "AddrAgency1": {"V": json.get("AddrAgency1", "")},
        "MailAgency1": {"V": json.get("MailAgency1", "")},
        "CityAgency1": {"V": json.get("CityAgency1", "")},
        "StateAgency1": {"V": json.get("StateAgency1", "")},
        "ZipAgency1": {"V": json.get("ZipAgency1", "")},
        # Agency 2
        "NameAgency2": {"V": json.get("NameAgency2", "")},
        "AddrAgency2": {"V": json.get("AddrAgency2", "")},
        "MailAgency2": {"V": json.get("MailAgency2", "")},
        "CityAgency2": {"V": json.get("CityAgency2", "")},
        "StateAgency2": {"V": json.get("StateAgency2", "")},
        "ZipAgency2": {"V": json.get("ZipAgency2", "")},
    }

    for i, record in enumerate(json.get("Offense Record", {}).get("Records", []), 1):
        offense_datetime = json.get("Case Information", {}).get("Offense Date", "")
        offense_date = offense_datetime.split("T")[0]

        data["Fileno:" + str(i)] = {"V": json.get("General", {}).get("File No", "")}
        data["ArrestDate:" + str(i)] = {"V": offense_date}
        data["Description:" + str(i)] = {"V": record.get("Description", "")}
        data["DOOF:" + str(i)] = {"V": offense_date}
        data["Disposition:" + str(i)] = {
            "V": json.get("Offense Record").get("Disposition Method")
        }
        data["DispositionDate:" + str(i)] = {
            "V": json.get("Offense Record").get("Disposed On")
        }

    return data
