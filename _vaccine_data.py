#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 08:16:17 2021

@author: raechen
"""


from requests import get
import pandas as pd


def _getAPIData(endpoint):
    response = get(endpoint)
    
    if response.status_code >= 400:
        raise RuntimeError(f'Request failed: { response.text }')
        
    return response.json()


def GetData(area_type='ltla', 
            date='2020-12-01',
            area_list = ["Manchester", "Trafford", "Bury", "Tameside", 
                         "Rochdale", "Salford", "Stockport", "Wigan", "Bolton", 
                         "Oldham"]):
    '''

    Returns
    -------
    data : DataFrame

    '''
    
    if area_type == 'msoa':
        data = pd.read_csv("https://api.coronavirus.data.gov.uk/"''
                           "v2/data?areaType=msoa&areaCode=E08000003&metric="''
                           "cumPeopleVaccinatedFirstDoseByVaccinationDate&"''
                           "metric=cumVaccinationFirstDoseUptakeByVaccinationDatePercentage&"''
                           "metric=cumPeopleVaccinatedCompleteByVaccinationDate&"''
                           "metric=cumPeopleVaccinatedSecondDoseByVaccinationDate&"''
                           "metric=cumVaccinationSecondDoseUptakeByVaccinationDatePercentage&"''
                           "format=csv")
    else:
        data_list = []
        for area in area_list:
            endpoint = (
                        'https://api.coronavirus.data.gov.uk/v1/data?'
                        'filters=areaType='+area_type+'; areaName='+area+'; date>='+date+'&'
                        'structure={"Date":"date","Area": "areaName"'
                                    ',"NewCases":"newCasesBySpecimenDate"'
                                    ',"TotalCases":"cumCasesBySpecimenDate"'
                                    ',"RegisteredPopulation":"VaccineRegisterPopulationByVaccinationDate"'
                                    ',"TotalFirstDose":"cumPeopleVaccinatedFirstDoseByVaccinationDate"'
                                    ',"TotalVaccinated":"cumPeopleVaccinatedCompleteByVaccinationDate"'
                                    ',"CoverageRate":"cumVaccinationCompleteCoverageByVaccinationDatePercentage"}'
                        )
            
            data = _getAPIData(endpoint)
            data = data['data']
            data_list.append(pd.DataFrame(data))
                
        data = pd.concat(data_list, ignore_index=True)
        data.Date = pd.to_datetime(data.Date, format='%Y-%m-%d')
    
    return data


