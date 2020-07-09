from dear_petition.petition import constants


cr_287 = {
    "County": "County",
    "OffenseFileNoRow": "Fileno:{idx}",
    "OffenseArrestDateRow": "ArrestDate:{idx}",
    "OffenseDescriptionRow": "Description:{idx}",
    "OffenseDOOFRow": "DOOF:{idx}",
    "OffenseDispositionRow": "Disposition:{idx}",
    "OffenseDispositionDateRow": "DispositionDate:{idx}",
}

cr_285 = cr_287.copy()
cr_285.update({"County": "CountyName"})

fields = {
    constants.MISDEMEANOR: {},  # TBD
    constants.ATTACHMENT: cr_285,
    constants.DISMISSED: cr_287,
    constants.NOT_GUILTY: {},  # TBD
}
