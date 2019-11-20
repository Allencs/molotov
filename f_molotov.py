from molotov import scenario


url = '***'


@scenario(weight=50)
async def scenario_one(session):
    """
    内部使用aiohttp的ClientSession()类
    注：请求返回的是ClientResponse对象，对象的text().json(),conten.read()等为可等待对象，
    需要配合使用await。
    :param session: ClientSession()实例
    :return: None
    """
    async with session.get(url) as req:
        await req.text(encoding='gb18030')
        assert req.status == 200
        # print("Response length: {}".format(len(response)))



