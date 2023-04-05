import os
import json
import time

import redis
from datetime import datetime
from dataclasses import dataclass, asdict
from clickhouse_driver import Client

# Define the Redis connection parameters
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_DB = int(os.environ.get("REDIS_DB", 0))

# Define the ClickHouse connection parameters
CLICKHOUSE_HOST = os.environ.get("CLICKHOUSE_HOST", 'clickhouse')
CLICKHOUSE_PORT = int(os.environ.get("CLICKHOUSE_PORT", 9000))
CLICKHOUSE_USER = os.environ.get("CLICKHOUSE_USER")
CLICKHOUSE_PASS = os.environ.get("CLICKHOUSE_PASS")


# Define the database and table names in ClickHouse
CLICKHOUSE_DB = os.environ.get("CLICKHOUSE_DB", 'destorestatistic')
CLICKHOUSE_TABLE = os.environ.get("CLICKHOUSE_TABLE", 'events')

# Define the dataclass for the events
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
    datacenter: str

def create_redis_client(host: str, port: int, db: int) -> redis.client.Redis:
    return redis.Redis(host=host, port=port, db=db)

def create_clickhouse_client(host: str, port: int, user: str, password: str) -> Client:
    return Client(host=host, port=port, user=user, password=password)

def save(client: Client, event: Event) -> bool:
    # Save the Event object in ClickHouse
    query = f"INSERT INTO {CLICKHOUSE_DB}.{CLICKHOUSE_TABLE} VALUES"
    event_data = [list(asdict(event).values())]
    try:
        client.execute(query, event_data, types_check=True)
        return True
    except Exception as err:
        print(f'[Error] - {datetime.now()} - {err}\n\n{event}')
        return False
    
def prepare_data(event: Event) -> Event:
    event.time = datetime.fromtimestamp(event.time)

    if not isinstance(event.category_code, str):
        event.category_code = None

    if not isinstance(event.brand, str):
        event.brand = None

    return event

def retrieve_and_save():
    r = create_redis_client(REDIS_HOST, REDIS_PORT, REDIS_DB)
    client = create_clickhouse_client(CLICKHOUSE_HOST, CLICKHOUSE_PORT, CLICKHOUSE_USER, CLICKHOUSE_PASS)

    # Loop through the Redis keys and retrieve the corresponding values
    for key in r.scan_iter("*"):
        redis_event: bytes = r.get(key)
        print(redis_event)
        json_event = json.loads(redis_event.decode('utf-8'))
        event = Event(*dict(json_event).values())
        r.delete(key)
        

        save(client, prepare_data(event))


    client.disconnect()



if __name__ == '__main__':
    retrieve_and_save()
    time.sleep(10)
