import re

from .utils import catch_parse_error


@catch_parse_error
def parse_defendant_name(soup):
    """
    Parse defendant name

    Sample HTML:

        <tr ng-repeat="party in ::roaSection.getPartiesByConnectionTypeId(connectionType.codeId)" class="roa-party-row roa-pad-b-10 ng-scope">
            <td class="roa-text-bold">
                <div ng-if="::$first" class="ng-binding ng-scope">Defendant</div>
            </td>
            <td ng-if="::roaSection.maxPartyCount == -1 || $scope.lessThan($index, roaSection.maxPartyCount)" class="ng-scope">
                <table class="roa-table roa-inline">
                    <tbody>
                        <tr>
                            <td ng-class="::roaSection.isInactive(party, connectionType.codeId) ? 'roa-text-italic' : 'roa-text-bold'" class="ng-binding roa-text-bold">
                                DOE, JANE LEE
                            </td>
                        </tr>
                    </tbody>
                </table>
    """  # noqa
    div = soup.find("div", string=re.compile(r"\s?Defendant\s?"))
    row = div.find_parent("tr")
    name = row.css.select_one("table.roa-table").text.strip()
    return name


@catch_parse_error
def parse_defendant_race(soup):
    """
    Parse race

    Sample HTML:
        <div ng-if="::party.Race" class="ng-binding ng-scope">
            White
        </div>
    """ # noqa
    race_div = soup.find('div', {'ng-if': '::party.Race'})
    if not race_div:
        return ""

    return race_div.get_text(strip=True)


@catch_parse_error
def parse_defendant_sex(soup):
    """
    Parse sex

    Sample HTML:
        <div ng-if="::party.Gender" class="ng-binding ng-scope">
            Female
        </div>
    """ # noqa
    sex_div = soup.find('div', {'ng-if': '::party.Gender'})
    if not sex_div:
        return ""

    return sex_div.get_text(strip=True)
