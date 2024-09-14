from types import SimpleNamespace
from typing import TYPE_CHECKING
from typing import Union
from typing import Callable

# from src.tools.retry import PrivateRetry
from src.interface.template import API
from src.testers import Params

if TYPE_CHECKING:
    from src.config import Parameter


class Search(API):
    search_params = (
        SimpleNamespace(
            api="https://www.douyin.com/aweme/v1/web/general/search/single/",
            count=15,
            channel="aweme_general",
            type="general",
        ),
        SimpleNamespace(
            api="https://www.douyin.com/aweme/v1/web/search/item/",
            count=20,
            channel="aweme_video_web",
            type="video",
        ),
        SimpleNamespace(
            api="https://www.douyin.com/aweme/v1/web/discover/search/",
            count=12,
            channel="aweme_user_web",
            type="user",
        ),
        SimpleNamespace(
            api="https://www.douyin.com/aweme/v1/web/live/search/",
            count=15,
            channel="aweme_live",
            type="live",
        ),
    )

    def __init__(
        self,
        params: Union["Parameter", Params],
        cookie: str = None,
        proxy: str = None,
        keyword: str = ...,
        tab=0,
        page=1,
        sort_type=0,
        publish_time=0,
        *args,
        **kwargs,
    ):
        super().__init__(
            params,
            cookie,
            proxy,
            *args,
            **kwargs,
        )
        self.keyword = keyword
        self.tab = tab
        self.page = page
        self.sort_type = sort_type
        self.publish_time = publish_time

    def generate_params(
        self,
    ) -> dict:
        return self.params | {
            "keyword": self.keyword,
            "tab": self.tab,
            "sort_type": self.sort_type,
            "publish_time": self.publish_time,
            "page": self.page,
        }

    async def run(
        self,
        referer: str = "",
        single_page=False,
        data_key: str = "aweme_list",
        error_text="",
        cursor="cursor",
        has_more="has_more",
        params: Callable = lambda: {},
        data: Callable = lambda: {},
        method="POST",
        headers: dict = None,
        *args,
        **kwargs,
    ):
        data = self.search_params[self.tab]

        self.set_referer("https://www.douyin.com/search")
        self.api = data.api

        # self.PC_headers["Referer"] = (
        #     f"https://www.douyin.com/search/{
        #     quote(
        #         self.keyword)}?" f"source=switch_tab&type={
        #     data.type}")
        # if self.tab in {2, 3}:
        #     deal = self._run_user_live
        # elif self.tab in {0, 1}:
        #     deal = self._run_general
        # else:
        #     raise ValueError
        print("Search.run")
        # with self.progress_object() as progress:
        #     task_id = progress.add_task("正在获取搜索结果数据", total=None)
        #     while not self.finished and self.page > 0:
        #         progress.update(task_id)
        #         await deal(data, self.tab)
        #         self.page -= 1

        # await self._run_general(data, self.tab)
        type_ = self.tab
        params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "search_channel": data.channel,
            "sort_type": self.sort_type,
            "publish_time": self.publish_time,
            "keyword": self.keyword,
            "search_source": "tab_search",
            "query_correct_type": "1",
            "is_filter_search": {True: 1, False: 0}[
                any((self.sort_type, self.publish_time))
            ],
            "from_group_id": "",
            "offset": self.cursor,
            "count": 10 if self.cursor else data.count,
            "pc_client_type": "1",
            "version_code": "170400" if type_ else "190600",
            "version_name": "17.4.0" if type_ else "19.6.0",
            "cookie_enabled": "true",
            "platform": "PC",
            "downlink": "10",
        }
        print("Search._run_general", params)
        # self.deal_url_params(params, 4 if self.cursor else 8)
        # print("Search._run_general agbus ", params)
        print("Search._run_general", self.headers)
        await self.run_single(
            data_key="data",
            error_text=" 出错了 搜索数据",
            cursor="cursor",
            has_more="has_more",
            params=lambda: params,
            # data=lambda: data,
            method="POST",
            headers=headers,
        )

        return self.response
        print("Search.run")
        return self.response

    async def _run_general(self, data: SimpleNamespace, type_: int, *args):
        pass
        # self._get_search_data(data.api, params, "data", finished=True)

    # @PrivateRetry.retry
    # def _get_search_data(self, api: str, params: dict, key: str):
    #     if not (
    #         data := self.send_request(
    #             api,
    #             params=params,
    #         )
    #     ):
    #         self.log.warning("获取搜索数据失败")
    #         return False
    #     try:
    #         self.deal_item_data(data[key])
    #         self.cursor = data["cursor"]
    #         self.finished = not data["has_more"]
    #         return True
    #     except KeyError:
    #         self.log.error(f"搜索数据响应内容异常: {data}")
    #         self.finished = True
    #         return False

    async def run_single(
        self,
        data_key: str = "data",
        error_text=" 出错了 搜索数据",
        cursor="max_cursor",
        has_more="has_more",
        params: Callable = lambda: {},
        data: Callable = lambda: {},
        method="POST",
        headers: dict = None,
        *args,
        **kwargs,
    ):
        await super().run_single(
            data_key,
            error_text,
            cursor,
            has_more,
            params,
            data,
            method,
            headers,
            *args,
            **kwargs,
        )
