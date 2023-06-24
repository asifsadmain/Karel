import torch

from .base_vae import BaseVAE
from .leaps_vae import LeapsVAE
from .sketch_vae import SketchVAE

def load_model(model_cls_name: str, model_args: dict,
               model_params_path: str = None) -> BaseVAE:
    model_cls = globals().get(model_cls_name)
    assert issubclass(model_cls, BaseVAE)
    model = model_cls(**model_args)
    if model_params_path is not None:
        model.load_state_dict(torch.load(model_params_path, map_location=model.device))
    return model
