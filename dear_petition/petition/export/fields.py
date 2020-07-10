from dear_petition.petition import constants


cr_287 = {
    "County": "County",
    "FileNo": "ConsJdgmntFileNum",
    "NamePetitioner": "NamePetitioner",
    "OffenseFileNoRow": "Fileno:{idx}",
    "OffenseArrestDateRow": "ArrestDate:{idx}",
    "OffenseDescriptionRow": "Description:{idx}",
    "OffenseDOOFRow": "DOOF:{idx}",
    "OffenseDispositionRow": "Disposition:{idx}",
    "OffenseDispositionDateRow": "DispositionDate:{idx}",
}

cr_285 = {
    "County": "CountyName",
    "FileNo": "FileNo",
    "NamePetitioner": "PetitionerName",
    "OffenseFileNoRow": "FileNoRow{idx}",
    "OffenseArrestDateRow": "ArrestDateRow{idx}",
    "OffenseDescriptionRow": "OffenseDescRow{idx}",
    "OffenseDOOFRow": "DateOfOffenseRow{idx}",
    "OffenseDispositionRow": "DispositionRow{idx}",
    "OffenseDispositionDateRow": "DispositionDateRow{idx}",
}

fields = {
    constants.MISDEMEANOR: {},  # TBD
    constants.ATTACHMENT: cr_285,
    constants.DISMISSED: cr_287,
    constants.NOT_GUILTY: {},  # TBD
}
