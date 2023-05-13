from sensoric.sinks import Sink
from copy import deepcopy
from time import time


DATA = [{'measurement': 'cpu', 'tags': {'sensor': 'cpu', 'host': 'hc'},
         'fields': {'thermal_zone3': 50.0, 'thermal_zone1': 53.0, 'thermal_zone4': 45.0, 'thermal_zone2': 54.0,
                    'thermal_zone0': 49.0, 'load': 0.10205078125}, 'time': 1683993702304858624},
        {'measurement': 'memory', 'tags': {'sensor': 'memory', 'host': 'hc'},
         'fields': {'total': 2088108032, 'available': 977645568, 'buffers': 99377152, 'cached': 678309888,
                    'swap_total': 2117787648, 'swap_used': 372506624}, 'time': 1683993702305519360},
        {'measurement': 'net', 'tags': {'sensor': 'net', 'host': 'hc'},
         'fields': {'wl_bytes_sent': 772968, 'wl_bytes_recv': 226908, 'wl_errin': 0, 'wl_errout': 0, 'wl_dropin': 0,
                    'wl_dropout': 0, '112_bytes_sent': 11853843852, '112_bytes_recv': 216239220, '112_errin': 62,
                    '112_errout': 0, '112_dropin': 0, '112_dropout': 11266, 'veth-de-local_bytes_sent': 163335487,
                    'veth-de-local_bytes_recv': 11306790487, 'veth-de-local_errin': 0, 'veth-de-local_errout': 0,
                    'veth-de-local_dropin': 0, 'veth-de-local_dropout': 0, 'cni-podman0_bytes_sent': 19292,
                    'cni-podman0_bytes_recv': 2220, 'cni-podman0_errin': 0, 'cni-podman0_errout': 0,
                    'cni-podman0_dropin': 0, 'cni-podman0_dropout': 0, 'eth0_bytes_sent': 1212626195,
                    'eth0_bytes_recv': 1009713489, 'eth0_errin': 0, 'eth0_errout': 0, 'eth0_dropin': 298158,
                    'eth0_dropout': 0}, 'time': 1683993702305972992},
        {'measurement': 'queue', 'tags': {'sensor': 'postfix_queue', 'host': 'hc'}, 'fields': {'postfix_queue': 0},
         'time': 1683993702320505856},
        {'measurement': 'net', 'tags': {'sensor': 'net', 'host': 'hc'},
         'fields': {'fritz_bytes_sent': 102753673921, 'fritz_bytes_recv': 293154356499, 'fritz_is_connected': 1,
                    'fritz_upstream': 14423, 'fritz_downstream': 261869, 'fritz_upstream_max': 5849625,
                    'fritz_downstream_max': 17753875}, 'time': 1683993702525872640}]

DATA2 = deepcopy(DATA)
DATA2[0]['fields']['thermal_zone1'] = 20


def test_no_filter():
    sink = Sink()
    assert not sink.filter_data(DATA)


def test_filter():
    print("...", DATA[0]['fields']['thermal_zone1'])
    sink = Sink(filter_expr="('{measurement}' == 'cpu') & ({fields[thermal_zone1]} > 50)")
    assert sink.filter_data(DATA)


def test_filter_flip():
    """
    Ensure that the filter needs to flip before another data pair is admitted.
    """
    sink = Sink(filter_expr="('{measurement}' == 'cpu') & ({fields[thermal_zone1]} > 50)", requires_flipped=True)
    assert sink.filter_data(DATA)
    assert not sink.filter_data(DATA)

    assert not sink.filter_data(DATA2)
    assert sink.filter_data(DATA)

def test_filter_data_delay():
    """
    Ensure that the filter only admits data after data delay has been met.
    """
    sink = Sink(filter_expr="('{measurement}' == 'cpu') & ({fields[thermal_zone1]} > 50)", data_delay=60)
    assert sink.filter_data(DATA)
    assert not sink.filter_data(DATA)
    assert not sink.filter_data(DATA)
    sink.last_warn = time() - 60
    assert sink.filter_data(DATA)
