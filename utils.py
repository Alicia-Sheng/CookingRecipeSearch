from typing import Dict, Union, Generator
import os
import json


def load_clean_wapo_with_embedding(
    wapo_jl_path: Union[str, os.PathLike]
) -> Generator[Dict, None, None]:
    """
    load wapo docs as a generator
    :param wapo_jl_path:
    :return: yields each document as a dict
    """
    f = open(wapo_jl_path)
    data = json.load(f)
    for d in data:
        
        yield d


if __name__ == "__main__":
    pass