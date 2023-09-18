# web_detect

https://github.com/xtekky/gpt4free





### 錯誤訊息

如果Ask_GPT沒辦法成功聯接並出現SSL error

請先確定Ask_GPT中的Provider為何，例如為```g4f.Provider.DeepAi```，接著請到lib中找到提供該函數的地方
在DeepAi.py底下找到一段程式碼

以我本身的電腦路徑```cd ~/.local/lib/python3.8/site-packages/g4f```

接著找到DeepAi這個py程式碼，```DeepAi.py```

其中一段程式碼如下

```
        payload = {"chas_style": "chat", "chatHistory": json.dumps(messages)}
        api_key = js2py.eval_js(token_js)
        headers = {
            "api-key": api_key,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        }
        async with ClientSession(
            headers=headers 
        ) as session:
            async with session.post("https://api.deepai.org/make_me_a_pizza", proxy=proxy, data=payload) as response:
                response.raise_for_status()
                async for stream in response.content.iter_any():
                    if stream:
                        yield stream.decode()
```
並將程式碼修改成
```
        payload = {"chas_style": "chat", "chatHistory": json.dumps(messages)}
        api_key = js2py.eval_js(token_js)
        headers = {
            "api-key": api_key,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        }
        connector = aiohttp.TCPConnector(ssl=False)
        async with ClientSession(
            headers=headers ,connector=connector
        ) as session:
            async with session.post("https://api.deepai.org/make_me_a_pizza", proxy=proxy, data=payload) as response:
                response.raise_for_status()
                async for stream in response.content.iter_any():
                    if stream:
                        yield stream.decode()
```

該程式碼即可正常執行，其原因是因為系統內建ssl庫憑證有誤，將其驗證進行關閉即可

#### 額外方法

若需要徹底解決該問題，可以到aiohttp庫中 

以自身系統為例，路徑可能取決於不同電腦的安裝系統路徑

```
cd ~/.local/lib/python3.8/site-packages/aiohttp
```

```
sudo nano connector.py
```

並且在```class TCPConnector(BaseConnector)```中可以找到```def __init__```函數

如下程式碼
```
def __init__(
        self,
        *,
        verify_ssl: bool = True,
        fingerprint: Optional[bytes] = None,
        use_dns_cache: bool = True,
        ttl_dns_cache: Optional[int] = 10,
        family: int = 0,
        ssl_context: Optional[SSLContext] = None,
        ssl: Union[None, bool, Fingerprint, SSLContext] = None,
        local_addr: Optional[Tuple[str, int]] = None,
        resolver: Optional[AbstractResolver] = None,
        keepalive_timeout: Union[None, float, object] = sentinel,
        force_close: bool = False,
        limit: int = 100,
        limit_per_host: int = 0,
        enable_cleanup_closed: bool = False,
        loop: Optional[asyncio.AbstractEventLoop] = None,
    ):
```
將ssl關閉，更改成以下程式碼
```
ssl: Union[None, bool, Fingerprint, SSLContext] = False,
```
儲存即可徹底解決Error問題