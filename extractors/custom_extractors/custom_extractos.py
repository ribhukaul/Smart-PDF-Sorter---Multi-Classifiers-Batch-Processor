from extractors.custom_extractors.waminsurance.kid_governance import WamInsuranceKidGovernanceExtractor
from extractors.custom_extractors.waminsurance.kid_module import WamInsuranceKidModuleExtractor
from extractors.custom_extractors.waminsurance.gkid_governance import WamInsuranceGKidGovernanceExtractor
from extractors.custom_extractors.waminsurance.kid_credem import WamInsuranceKidCredemExtractor
from extractors.custom_extractors.wamasset.fullkid import WamAssetKidExtractor

from extractors.custom_extractors.wamderivati.complexity import WamDerivatiComplexity
from extractors.custom_extractors.wambond.bloombergss import WamBondBloombergSS

# SWITCH CASE FOR EXTRACTION MODEL SELECTION
custom_extractors = {
        'waminsurance': {
            'kidgovernance': WamInsuranceKidGovernanceExtractor,
            'gkidgovernance': WamInsuranceGKidGovernanceExtractor,
            'kidcredem': WamInsuranceKidCredemExtractor,
            'kidmodule':  WamInsuranceKidModuleExtractor            
            },
        'wamderivati': {
            'complexity': WamDerivatiComplexity,
            'productionderivatives':''
            },
        'wamfondi': {
            'peergroup': ''
        },
        'wambond': {
            'bloombergss': WamBondBloombergSS
        },
        'wamasset':{
            'kidasset': WamAssetKidExtractor
        },
        'sim':{}
    }