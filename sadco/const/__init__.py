from enum import Enum


class SurveyType(str, Enum):
    """Survey Types."""
    HYDRO = 'Hydro'
    CURRENTS = 'Currents'
    WEATHER = 'Weather'
    WAVES = 'Waves'
    ECHOSOUNDING = 'Echo-Sounding'
    UTR = 'UTR'
    VOS = 'VOS'
    UNKNOWN = 'Unkown'
