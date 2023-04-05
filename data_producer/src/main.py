import os
import uuid
import json
import random
from time import sleep
from typing import Any, Generator
from dataclasses import dataclass, asdict
from datetime import datetime

import pandas as pd
import redis

FILE_PATH = 'events.csv'

EVENT_COUNT = int(os.environ.get("EVENT_COUNT", 500))
DATACENTER = os.environ.get("DATACENTER")
GENERATOR_SPEED_COEFICIENT = float(os.environ.get("GENERATOR_SPEED_COEFICIENT", 0.05))
REDIS_EXPIRATION_IN_SEC = int(os.environ.get("REDIS_EXPIRATION_IN_SEC", 600))

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_DB = int(os.environ.get("REDIS_DB", 0))

@dataclass
class Event:
    time: datetime
    type: str
    product_id: int
    category_id: int
    category_code: str | None
    brand: str | None
    price: float
    user_id: int
    user_session: str


def read_data() -> pd.DataFrame:
    df = pd.read_csv(FILE_PATH)
    return df

def generate_events(df: pd.DataFrame, count: int) -> Generator[Event, None, None]:
    count *= 2
    data = df.sample(count)
    rows = [*data.itertuples(index=False, name=None)]
    pointer_1, pointer_2 = 0, count-1

    while pointer_1 < pointer_2:
        product_data = rows[pointer_1]
        user_data = rows[pointer_2]
        yield Event(*product_data[0: len(product_data)-2], *user_data[len(user_data)-2::])
        pointer_1 += 1
        pointer_2 -= 1

def create_redis_client(host: str, port: int, db: int) -> redis.client.Redis:
    return redis.Redis(host=host, port=port, db=db)

def upload_event_to_redis(client: redis.client.Redis, event: Event, expire_sec: int = 600) -> bool:
    event = asdict(event)
    event['datacenter'] = DATACENTER
    key = str(uuid.uuid4())
    client.setnx(key, dict_to_bytes(event))
    client.expire(key, expire_sec)
    return True

def dict_to_bytes(data: dict) -> bytes:
    return bytes(json.dumps(data), 'utf-8')

if __name__ == "__main__":
    df = read_data()
    print(f"[INFO] Load {len(df)} rows")

    r = create_redis_client(REDIS_HOST, REDIS_PORT, REDIS_DB)
    print(f"[INFO] Initial redis client {r}")
    print(f"[INFO] Generate {EVENT_COUNT} events. Start process . . .")
    
    done_events = 0
    for event in generate_events(df, EVENT_COUNT):
        event.time = datetime.now().timestamp()
        upload_event_to_redis(r, event, REDIS_EXPIRATION_IN_SEC)
        sleep(random.random() / GENERATOR_SPEED_COEFICIENT)
        done_events += 1
        print(f"[INFO] {done_events} events already sent from {EVENT_COUNT}")

    print(f"[INFO] Process Complete !")



