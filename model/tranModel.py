import json
import requests as rt
import torch
import torchaudio
from seamless_communication.models.inference import Translator
class tranModels(object):
    def __init__(self):
        pass

    @classmethod
    def tranPredict(cls,mtext,typ,trg,src):
        translator =  Translator("seamlessM4T_large", "vocoder_36langs", torch.device("cuda:1"), torch.float16)

        translated_text, _, _ = translator.predict(mtext,typ, trg, src)
    
        return translated_text
trmodel = tranModels()
