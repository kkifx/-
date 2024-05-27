import requests
import re

# 设置HTTP代理
proxies = {
    'http': 'http://127.0.0.1:10809',
    'https': 'http://127.0.0.1:10809',
}

# 请求链接
base_url = "https://raw.githubusercontent.com/mermeroo/V2RAY-and-CLASH-Subscription-Links/main/SUB%20LINKS"

# 发送GET请求
response = requests.get(base_url, proxies=proxies)

# 检查请求是否成功
if response.status_code == 200:
    # 分割文本内容为行
    lines = response.text.split('\n')

    # 正则表达式匹配URL
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    # 过滤不含"github"的链接并验证URL格式
    valid_links = [line for line in lines if "github" not in line and url_pattern.match(line.strip())]

    # 将所有https替换为http
    http_links = [link.replace('https:', 'http:') for link in valid_links]

    # 初始化Base64内容的字符串
    base64_content = ''

    for link in http_links:
        # 对每个链接发起GET请求
        link_response = requests.get(link, proxies=proxies)

        # 检查请求是否成功
        if link_response.status_code == 200:
            # 检查内容是否包含Base64编码
            if b'base64,' in link_response.content:
                # 直接添加Base64内容，不需要解码
                base64_content += link_response.content.decode('utf-8') + '\n'

    # 打印Base64内容
    if base64_content:
        print(base64_content)
    else:
        print("没有找到Base64编码的内容.")
else:
    print(f"请求失败，状态码：{response.status_code}")
