from clarify import *
import datetime
import os

v1_url = "http://results.enr.clarityelections.com/NJ/Cape_May/71890/190686/Web01/en/summary.html"

v2_url = "http://results.enr.clarityelections.com/NJ/Mercer/71882/Web02/#/"

# fighting pycharm :/
if 'tests' in os.getcwd().split('/'):
    test_data_dir = 'data/'
else:
    test_data_dir = 'tests/data/'


# test if jurisdiction auto_downloads
def test_jurisdiction_parse():
    """
    Issue #1 DONEEEEE
    """
    j = Jurisdiction(v1_url, 'county')
    p = Parser()
    p.from_jurisdiction(j)
    assert p.region == 'Cape May'

    j2 = Jurisdiction(v2_url, 'county')
    p.from_jurisdiction(j2)
    assert p.region == 'Mercer'

def test_backwards_compatibility():
    er = Parser()
    er.parse(test_data_dir + 'precinct.xml')
    assert er.region == 'Greenup'


def test_precinct_parser():
    num_precincts = 33
    num_candidates = 5
    # Overvotes and undervotes
    num_pseudo_candidates = 2
    num_expected_results = (num_candidates * (num_precincts + 1) +
                            num_pseudo_candidates * (num_precincts + 1))

    er = Parser()
    er.parse(test_data_dir + 'precinct.xml')

    assert er.timestamp.replace(tzinfo=None) == datetime.datetime(2014, 5, 20, 20, 19, 21)
    assert er.election_name == "2014 Primary Election"
    assert er.election_date== datetime.date(2014, 5, 20)
    assert er.region== "Greenup"
    assert er.total_voters == 28162
    assert er.ballots_cast == 5926
    assert er.voter_turnout == 21.04

    assert len(er.result_jurisdictions) ==  num_precincts
    precinct = next(p for p in er.result_jurisdictions if p.name == 'A105')
    assert precinct.total_voters == 0
    assert precinct.ballots_cast == 171
    assert precinct.voter_turnout == 0
    assert precinct.percent_reporting == 4

    assert len(er.contests) == 1

    assert len(er.results) == num_expected_results


def test_county_parser():
    num_counties = 75
    num_candidates = 1
    # Election
    num_vote_types = 4
    num_expected_results = (num_vote_types * num_counties * num_candidates) + (num_vote_types * num_candidates)

    er = Parser()
    er.parse(test_data_dir + 'county.xml')
    assert er.timestamp.replace(tzinfo=None), datetime.datetime(2014, 11, 13, 14, 58, 41)
    assert er.election_name == "2014 General Election"
    assert er.election_date == datetime.date(2014, 11, 4)
    assert er.region == "AR"
    assert er.total_voters == 1690577
    assert er.ballots_cast == 850615
    assert er.voter_turnout == 50.32

    assert len(er.result_jurisdictions) == num_counties
    county = next(c for c in er.result_jurisdictions if c.name == 'Arkansas')
    assert county.total_voters ==  10196
    assert county.ballots_cast == 5137
    assert county.voter_turnout == 50.38
    assert county.precincts_participating == 30
    assert county.precincts_reporting_percent == 100.0

    assert len(er.contests) == 1

    assert len(er.results) == num_expected_results


