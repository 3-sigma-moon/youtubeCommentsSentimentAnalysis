from dataclasses import dataclass
from typing import Dict, List


@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)
class Comments:
    comments: List[str]
    continuation_token: str
    number_of_comments: int
    status: Dict

