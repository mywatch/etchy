import csv
import json
from typing import Any, Dict, Iterator, List, TextIO, Tuple

import click
from redis import Redis

# redis instance
redis: Redis = None


def store_data(columns_data: List[Tuple[str, str]]):
    """ write data into redis """
    for i in columns_data:
        redis.set(i[0], i[1])


def null_to_string(data: Dict) -> Dict:
    """ convert None values to <NULL> for saving into redis """
    s = "<NULL>"
    for k, v in data.items():
        if data[k] is None:
            data[k] = s
    return data


def string_to_null(data: Dict) -> Dict:
    """ convert <NULL> values to null for saving into redis """
    s = "<NULL>"
    for k, v in data.items():
        if data[k] == s:
            data[k] = None
    return data


def flatten(data: Dict, prefix='') -> Dict:
    """ Flatten dict. Nested key is expressed as 'nested:key' """
    result = {}
    for k, v in data.items():
        prefixed = f'{prefix}:{k}' if prefix else ""
        if isinstance(v, dict):
            result.update(flatten(data[k], prefixed or k))
        else:
            result[prefixed or k] = v
    return result


def decompose(k: str, v: Any) -> Dict:
    if ':' in k:
        k1, k2 = k.split(':', maxsplit=1)
        return {k1: decompose(k2, v)}
    else:
        return {k: v}


def merge(d1: Dict, d2: Dict) -> None:
    """ Merge two dictionary recursively """
    for k, v in d2.items():
        if k in d1:
            merge(d1[k], d2[k])
        else:
            d1[k] = v


def unflatten(data: Dict) -> Dict:
    """ Unflatten dict. """

    result: Dict = {}
    for k, v in data.items():
        merge(result, decompose(k, v))
    return result


def to_csv(f: TextIO, keys: Iterator) -> None:
    for i, key in enumerate(keys):
        data = flatten(json.loads(redis.get(key).decode()))
        csv_writer = csv.DictWriter(f, fieldnames=['key'] + list(data.keys()))
        data.update({'key': key.decode()})
        if i == 0:
            csv_writer.writeheader()
        csv_writer.writerow(null_to_string(data))


def to_json(f: TextIO, keys: Iterator) -> None:
    data = []
    for key in keys:
        # To display `redis_key` at left, create a dict
        # then update with loaded dict.
        d = {'redis_key': key.decode()}
        loaded: Dict = json.loads(redis.get(key).decode())
        d.update(loaded)
        data.append(d)
    json.dump(data, f)


def from_csv(f: TextIO) -> None:
    csv_data = csv.DictReader(f)
    columns_data: List[Tuple[str, str]] = []
    for row in csv_data:
        key = row['key']
        del row['key']
        value = json.dumps(unflatten(string_to_null(row)), separators=(',', ':'))
        columns_data.append((key, value))
    store_data(columns_data)


def from_json(f: TextIO) -> None:
    columns_data: List[Tuple[str, str]] = []
    for data in json.load(f):
        key = data['redis_key']
        del data['redis_key']
        value = json.dumps(data)
        columns_data.append((key, value))
    store_data(columns_data)


def export_data(filename: str, key_pattern: str, format: str = ''):
    """ read from redis and write to csv """

    if key_pattern is None:
        print(f'For writing to csv file, redis-key value is required')
        return

    with open(filename, 'w', newline='') as file:
        f = globals().get('to_' + format)
        if not f:
            print(f'No such format type: {format}.')
            return
        f(file, redis.scan_iter(match=key_pattern))


def import_data(filename: str, *args, format: str = ''):
    """ read from csv and write to redis """
    with open(filename, newline='', encoding='utf-8') as file:
        f = globals().get('from_' + format)
        if not f:
            print(f'No such format type: {format}.')
            return
        f(file)


@click.command()
@click.argument('cmd', type=click.Choice(['export', 'import']))
@click.argument('key', required=False)
@click.option('-f', '--filename', default="data", help='Output/Input file name')
@click.option('-h', '--host', default="localhost", help='Redis server host name')
@click.option('-p', '--port', default=6379, help='Redis server port number')
@click.option('-F', '--format', type=click.Choice(['json', 'csv']), default='json', help='Output format')
def main(cmd: str, key: str, filename: str, host: str, port: int, format: str):
    global redis
    redis = Redis(host=host, port=port)
    f = globals().get(cmd + '_data')
    if not filename.lower().endswith(('json', 'csv')):
        filename = f'{filename}.{format}'
    if f:
        f(filename, key, format=format)


if '__main__' == __name__:
    main()
