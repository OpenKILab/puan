from abc import ABC, abstractmethod
import aiohttp
import asyncio
from aiomultiprocess import Pool

from aiohttp_retry import RetryClient, ExponentialRetry

class BaseLLMModel(ABC):
    def __init__(self):
        self._is_initilized = False

    def initialize(self):
        self._is_initilized = True

    @abstractmethod
    def generate(self, prompt, messages, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def parse(self, response):
        raise NotImplementedError()

    async def response(
        self,
        prompt,
        messages,
        *args,
        num_trials=3,
        **kwargs,
    ):
        if not self._is_initilized:
            self.initialize()

        success, trials, errors = False, 0, []
        while (not success) and (trials < num_trials):
            try:
                response = None
                response = await self.generate(prompt, messages, *args, **kwargs)
                success, generated_text = self.parse(response)
                if not success:
                    raise Exception("An error occured!")
            except Exception as ex:
                generated_text = (
                    f"\n[Error] {type(ex).__name__}: {ex}\n[Response] {response}\n"
                )
                errors.append(generated_text)
                raise Exception(generated_text)
            finally:
                trials += 1

        if not success:
            generated_text = "".join(errors)
            raise Exception(generated_text)

        return {
            "success": success,
            "trials": trials,
            "prompt": prompt,
            "messages": messages,
            "generated_text": generated_text,
        }

# post task
async def _post(req):
    async with aiohttp.ClientSession() as session:
        async with session.post(req["url"], headers=req["headers"], data=req["data"]) as response:
            # 处理响应
            result = await response.json()
    return result

class HTTPAPILLMModel(BaseLLMModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = None
        self.headers = None
        # 指数增长 retry
        # retry_options = ExponentialRetry(attempts = 2 ** 2, start_timeout = 1.0)
        retry_options = ExponentialRetry(attempts = 0, start_timeout = 300.0)
        
        # 不同平台 不同 QPS
        self._qps = 4
        self.semaphore = asyncio.Semaphore(self._qps)
    
    # def __del__(self):
        # loop = asyncio.get_running_loop()
        # loop.create_task(self.cleanup())
    
    @property
    def qps(self):
        return self._qps
    
    @qps.setter
    def qps(self, new_qps):
        self._qps = new_qps
        self.semaphore = asyncio.Semaphore(self._qps)
        
    
    # 关闭 client session
    async def cleanup(self):
        await self.retry_client.close()
        
    # # aiomultiprocess 处理 post task
    # async def async_post(self, url, headers, data):
    #     req = [{"url": url, "headers": headers, "data": data}]
    #     async with Pool() as pool:
    #         results = await pool.map(_post, req)
    #     return results[0]
    
    async def async_post(self, url, headers, data, cookies=None, timeout=0, _is_stream=False):
        async with self.semaphore:
            retry_client = RetryClient(raise_for_status=False, retry_options=self.retry_options)
            async with retry_client.post(url, headers=headers, data=data, cookies=cookies, timeout=timeout) as response:
                # 处理响应
                try:
                    if _is_stream:
                        result = await response
                    else:
                        result = await response.json()
                except Exception as e:
                    result = await response.text()
        return result

