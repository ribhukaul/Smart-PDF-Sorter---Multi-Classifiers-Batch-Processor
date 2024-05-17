# tenenat -> prompt, tags, wordrepresentation
# extractor -> prompt, tags, wordrepresentation
from .tags import general_tags, kid_tags, gkid_tags
from .prompts import general_prompts, kid_prompts, gkid_prompts
from extractors.configs.extraction_config.tags.waminsurance import waminsurance_tags
from .word_representation import kid_wr, gkid_wr


extraction_configurations = {
    'general':{
        'word_representation':{
        },
        'prompts':{
        },
        'tags':{
            'doc_language': general_tags.DocLanguage,
        },            
    },
    # WAMINSURANCE
    'waminsurance':{
        'general':{
            'word_representation':{
                'performance': kid_wr.performance,
                'riy': kid_wr.riy,
                'costi_ingresso': kid_wr.costi_ingresso,
                'costi_gestione': kid_wr.costi_gestione                
            },
            'prompts':{
                'general_info': kid_prompts.general_info,
                'performance': kid_prompts.performance1y,
                'target_market': kid_prompts.market,
            },
            'tags':{
                'general_info': kid_tags.InformazioniBase,
                'scenari_performance': kid_tags.TabellaScenariPerformance,
                'riy': kid_tags.TabellaRiy,
                'costi_ingresso': kid_tags.TabellaCostiIngresso,
                'costi_gestione': kid_tags.TabellaCostiGestione,
            },            
        },
        'kid_governance':{
            'word_representation':{
            },
            'prompts':{
            },
            'tags':{
                'general_info': waminsurance_tags.InformazioniBaseKidGov
                }
        },
        'kid_credem':{
            'word_representation':{
            },
            'prompts':{
            },
            'tags':{
                'scenari_performance': waminsurance_tags.TabellaScenariPerformanceCredem,
            }
            
        },
        'kid_module':{
            'word_representation':{
            },
            'prompts':{
            },
            'tags':{
            }
        },
        'gkid_governance':{
            'word_representation':{'performance': kid_wr.performance,
                'costi_ingresso': gkid_wr.costi_ingresso_gkid,
                'costi_gestione': gkid_wr.costi_gestione_gkid
            },
            'prompts':{
            },
            'tags':{
            }
        }
    },
    # WAMDERIVATI
    'wamderivati':{
        'general':{
            'word_representation':{
            },
            'prompts':{
            },
            'tags':{
                
            },            
        },
        'complexity':{
            'word_representation':{
            },
            'prompts':{
            },
            'tags':{
                'general_info': waminsurance_tags.InformazioniBaseKidGov
                }
        }
}
