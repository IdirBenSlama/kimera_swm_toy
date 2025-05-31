from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4
from typing import Tuple

@dataclass
class Scar:
    scar_id: str
    gid_pair: Tuple[str, str]
    weight: float
    timestamp: datetime


SCAR_LOG = {}

def create_scar(g1, g2, weight):
    s = Scar(str(uuid4()), (g1.gid, g2.gid), weight, datetime.utcnow())
    SCAR_LOG[s.scar_id] = s
    g1.scars.append(s.scar_id)
    g2.scars.append(s.scar_id)
    return s


def fetch_scars(g1, g2):
    ids = set(g1.scars) | set(g2.scars)
    return [SCAR_LOG[i] for i in ids]
