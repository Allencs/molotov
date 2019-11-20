"""

This Molotov script has:

- a global setup fixture that sets variables
- an init worker fixture that sets the session headers
- an init session that attachs an object to the current session
- 1 scenario
- 2 tear downs fixtures

"""
import molotov


class Daemon(object):
    """Does something smart in real life with the async loop.
    """
    def __init__(self, loop):
        self.loop = loop

    def cleanup(self):
        pass


@molotov.global_setup()
def init_test(args):
    """
    Called once when the test starts.Set up some fixtures that are shared by all workers
    :param args: args arguments used to start Molotov
    :return: None
    """
    molotov.set_var('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36')
    molotov.set_var('endpoint', 'https://www.dy2018.com')


@molotov.setup()
async def init_worker(worker_num, args):
    """
    Called once per worker startup
    Caution: The decorated function should be a coroutine
    :param worker_num: worker_id the worker number
    :param args: args arguments used to start Molotov
    :return:
    """
    headers = {'AnotherHeader': '1',
               'User-Agent': molotov.get_var('User-Agent')}
    return {'headers': headers}


@molotov.setup_session()
async def init_session(worker_num, session):
    """
    Called once per worker startup
    Caution: The decorated function should be a coroutine
    :param worker_num: worker_id the worker number
    :param session: session the aiohttp.ClientSession instance created
    :return:
    """
    session.ob = Daemon(loop=session.loop)


@molotov.scenario(100, delay=3)
async def scenario_one(session):
    endpoint = molotov.get_var('endpoint')
    async with session.get(endpoint) as resp:
        # res = await resp.json()
        # assert res['result'] == 'OK'
        assert resp.status == 200


@molotov.teardown_session()
async def end_session(worker_num, session):
    """
    Called once per worker when the session is closing
    Caution: The decorated function should be a coroutine
    :param worker_num: worker_id the worker number
    :param session: session the aiohttp.ClientSession instance
    :return:
    """
    session.ob.cleanup()


@molotov.teardown()
def end_worker(worker_num):
    """
    Called when a worker is done
    :param worker_num: worker_id the worker number
    :return:
    """
    print("This is the end for %d" % worker_num)


@molotov.global_teardown()
def end_test():
    """
    Called when everything is done
    :return:
    """
    print("This is the end of the test.")


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
async def show_worker(event, **workers):
    if event == 'current_workers':
        print("=>")


@molotov.events()
async def print_request(event, **info):
    """
    all events are printed out
    :param event:
    :param info:
    :return:
    """
    if event == 'sending_request':
        print("=>")


"""同步请求
from molotov import global_setup, json_request, set_var


@global_setup(args)
def _setup():
    set_var('token', json_request('http://example.com')['content'])
"""