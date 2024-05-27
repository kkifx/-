import binascii
import concurrent

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import re
import base64
from concurrent.futures import ThreadPoolExecutor
from typing import Optional


# 函数定义
def is_base64_encoded(content):
    # 判断内容是否符合Base64编码的特征
    try:
        base64.b64decode(content)
        return True
    except (binascii.Error, ValueError):
        return False


def process_link(link: str, proxies: dict) -> Optional[str]:
    # 对每个链接发起GET请求
    link_response = requests.get(link, proxies=proxies, timeout=10)

    # 检查请求是否成功
    if link_response.status_code == 200:
        content_type = link_response.headers.get('Content-Type', '')
        # 检查内容类型是否为HTML，如果是则跳过
        if 'text/html' in content_type.lower():
            # 检查响应内容是否以"proxies:"开头，如果是则跳过
            if link_response.text.startswith('proxies:'):
                return None
            # 检查内容是否是Base64编码
            if is_base64_encoded(link_response.content):
                # 返回Base64内容
                return base64.b64decode(link_response.text).decode("utf-8")
    return None


# 设置HTTP代理
proxies = {
    'http': 'http://127.0.0.1:10809',
    'https': 'http://127.0.0.1:10809',
}

# 创建Retry对象，设置重试次数和间隔
retry_strategy = Retry(
    total=5,  # 总共尝试5次
    backoff_factor=0.5,  # 每次重试之间等待0.5秒
    status_forcelist=[500, 502, 503, 504],  # 针对这些HTTP状态码进行重试
    allowed_methods=["GET", "POST"]  # 只对GET和POST请求进行重试
)

# 创建HTTPAdapter并附加重试策略
adapter = HTTPAdapter(max_retries=retry_strategy)

# 创建Session实例并添加适配器
session = requests.Session()
session.mount('http://', adapter)
session.mount('https://', adapter)

# 请求链接
base_url = "https://raw.githubusercontent.com/mermeroo/V2RAY-and-CLASH-Subscription-Links/main/SUB%20LINKS"

# 发送GET请求
response = session.get(base_url, proxies=proxies)

# 检查请求是否成功
if response.status_code == 200:
    # 分割文本内容为行
    lines = response.text.split('\n')

    # 正则表达式匹配URL
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    # 过滤不含"github"的链接并验证URL格式
    valid_links = [line for line in lines if
                   "github" not in line and url_pattern.match(line.strip()) and "api" in line and not line.endswith(
                       "?")]

    # 将所有https替换为http
    http_links = [link.replace('https:', 'http:') for link in valid_links]

    with open('links.txt', 'w', encoding='utf-8') as ff:
        for http_link in http_links:
            ff.write(http_link + '\n')

    # 初始化Base64内容的字符串
    base64_content = ""

    # 使用多线程处理链接
    with ThreadPoolExecutor(max_workers=100) as executor:
        future_to_link = {executor.submit(process_link, link, proxies): link for link in http_links}
        for future in concurrent.futures.as_completed(future_to_link):
            link = future_to_link[future]
            try:
                result = future.result()
                if result:
                    base64_content += result
            except Exception as exc:
                print(f"处理链接{link}时出错: {exc}")

    # 将结果保存到文件
    with open('res.txt', 'w', encoding='utf-8') as f:
        if base64_content:
            f.write(base64_content)

else:
    print(f"请求失败，状态码：{response.status_code}")
