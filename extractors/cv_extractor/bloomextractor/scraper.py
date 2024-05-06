from typing import Dict
from extractors.cv_extractor.bloomextractor.DES.DesFieldExtractor import DesFieldExtractor
from extractors.cv_extractor.bloomextractor.CPN.CpnFieldsExtractor import CpnFieldsExtractor
from extractors.cv_extractor.bloomextractor.utils import recognize_image_type




def extract_data_from_ss(image_path: str, parallel: bool=False) -> Dict[str, str]:

    ss_type =recognize_image_type(image_path)
    print("ss_type:", ss_type)

    if ss_type == "DES":
        extractor = DesFieldExtractor(image_path)
        if parallel:
            extractor.extract_all_parallel()
        else:
            extractor.extract_all()
    
    
    elif ss_type == "CPN":
        extractor = CpnFieldsExtractor(image_path)
        extractor.extract_all()

    results = {
        "type": ss_type,
        "info": extractor.info
    }

    return results

