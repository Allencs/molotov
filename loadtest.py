import time

from molotov import scenario
import molotov


_API = 'http://localhost:8080/pftest/myApi/token'


_T = {}
_workers = {"works": 0}
_scenario = {"scenario": None}


def _now():
    return time.time() * 1000


@scenario(weight=100)
async def scenario_one(session):
    async with session.get(_API) as resp:
        res = await resp.text()
        if len(res) > 100:
            assert True


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Current supported events and their keyword arguments:
sending_request: session, request
response_received: session, response, request
current_workers: workers
scenario_start: scenario, wid
scenario_success: scenario, wid
scenario_failure: scenario, exception, wid
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


@molotov.events()
async def show_worker(event, **info):
    """
    current number of workers, it is tuple
    :param event: molotov event
    :param info:
    :return:
    """
    if event == 'current_workers':
        if _workers['works'] != info['workers']:
            _workers['works'] = info['workers']
            print("hi, current number of works is {}\n".format(_workers['works']))


@molotov.events()
async def scenario_info(event, **info):
    """
    info receives variable like {'wid': 0, 'scenario': {'name': 'scenario_one', 'weight': 100,
    'delay': 0.0, 'func': <function scenario_one at 0x000001787C341BF8>, 'args': (), 'kw': {}}}
    :param event:
    :param info:
    :return:
    """
    if event == 'scenario_start':
        if _scenario['scenario'] != info['scenario']['name']:
            _scenario['scenario'] = info['scenario']['name']
            print("***scenario [{}] is running\n".format(_scenario['scenario']))


'''
@molotov.events()
async def show_scenario_success(event, **info):
    """
    the format of info receives variable is the same as scenario_start
    :param event:
    :param info:
    :return: 
    """
    if event == 'scenario_success':
        print("%%%{}".format(info))
'''


@molotov.events()
async def record_time(event, **info):
    req = info.get('request')
    if event == 'sending_request':
        _T[req] = _now()
    elif event == 'response_received':
        _T[req] = _now() - _T[req]


@molotov.global_teardown()
def display_average():
    average = sum(_T.values()) / len(_T)
    TPS = float(len(_T) / (sum(_T.values()) / 1000))
    print("===============================================")
    print("+++Average ResponseTime %dms" % average)
    print("+++TPS %.2f" % TPS)
    print("===============================================")
