from .base_search import BaseSearch
from .latent_cem import LatentCEM
from .simulated_annealing import SimulatedAnnealing
from .latent_simulated_annealing import LatentSimulatedAnnealing
from .top_down import TopDownSearch

def get_search_cls(search_cls_name: str) -> BaseSearch:
    search_cls = globals().get(search_cls_name)
    assert issubclass(search_cls, BaseSearch)
    return search_cls
