from etchy import decompose, flatten, merge, unflatten


def test_flatten_simple():
    d = {'name': 'hoge'}
    assert d == flatten(d)

    d = {'name': 'hoge', 'nested': {'name': 'hoge'}}
    expected = {'name': 'hoge', 'nested:name': 'hoge'}
    assert expected == flatten(d)

    d = {'name': 'hoge', 'nested': {'name': 'hoge', 'nested': {'name': 'hoge'}}}
    expected = {'name': 'hoge', 'nested:name': 'hoge', 'nested:nested:name': 'hoge'}
    assert expected == flatten(d)


def test_flatten_complex():
    d = {
        'name': 'hoge',
        'nested': {
            'name': 'hoge',
            'nested': {
                'name': 'hoge',
                'dt': {
                    'date': {
                        'year': 2019,
                        'month': 2,
                        'day': 15
                    },
                    'time': {
                        'hour': 7,
                        'minute': 20,
                        'second': 30,
                        'microsecond': 12345
                    }
                }
            }
        }
    }
    expected = {
        'name': 'hoge',
        'nested:name': 'hoge',
        'nested:nested:name': 'hoge',
        'nested:nested:dt:date:year': 2019,
        'nested:nested:dt:date:month': 2,
        'nested:nested:dt:date:day': 15,
        'nested:nested:dt:time:hour': 7,
        'nested:nested:dt:time:minute': 20,
        'nested:nested:dt:time:second': 30,
        'nested:nested:dt:time:microsecond': 12345
    }
    assert expected == flatten(d)


def test_unflatten_simple():
    d = {'name': 'hoge', 'nested:name': 'hoge', 'nested:nested:name': 'hoge'}
    expected = {'name': 'hoge', 'nested': {'name': 'hoge', 'nested': {'name': 'hoge'}}}
    assert expected == unflatten(d)


def test_unflatten_complex():
    d = {
        'dt:date:year': 2019,
        'dt:date:month': 2,
        'dt:date:day': 15,
        'dt:time:hour': 7,
        'dt:time:minute': 20,
        'dt:time:second': 30,
        'dt:time:microsecond': 12345
    }
    expected = {
        'dt': {
            'date': {
                'year': 2019,
                'month': 2,
                'day': 15
            },
            'time': {
                'hour': 7,
                'minute': 20,
                'second': 30,
                'microsecond': 12345
            }
        }
    }
    assert expected == unflatten(d)


def test_decompose():
    assert {'nested': {'nested': {'dt': {'date': {'year': 2019}}}}} == decompose('nested:nested:dt:date:year', 2019)


def test_merge():
    d = {}
    merge(d, {'nested': {'nested': {'dt': {'date': {'year': 2019}}}}})
    assert d == {'nested': {'nested': {'dt': {'date': {'year': 2019}}}}}

    merge(d, {'nested': {'nested': {'dt': {'date': {'month': 2}}}}})
    assert d == {'nested': {'nested': {'dt': {'date': {'month': 2, 'year': 2019}}}}}

    merge(d, {'nested': {'nested': {'dt': {'date': {'day': 15}}}}})
    assert d == {'nested': {'nested': {'dt': {'date': {'day': 15, 'month': 2, 'year': 2019}}}}}
