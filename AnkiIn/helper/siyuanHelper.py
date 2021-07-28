import requests
import json
import re


API_URL = "http://127.0.0.1:6806/api/"
HEADERS = {"Content-Type": "application/json"}
AuthCookie = ""


def post(url: str, **params):
    try:
        response = requests.post(url, data=json.dumps(
            params), cookies={"siyuan": AuthCookie})
        return response
    except Exception:
        raise Exception


class ApiException(Exception):
    pass


class AuthCodeIncorrectException(Exception):
    pass


def parse_ial(text: str):
    ret = {}
    subs = re.finditer(r" (.+?)=\"(.+?)\"", text)
    for sub in subs:
        ret[sub.group(1)] = sub.group(2)
    return ret


def login(password: str):
    res = post(API_URL + "system/loginAuth", authCode=password)
    if res.json()["code"] != 0:
        raise AuthCodeIncorrectException
    global AuthCookie
    AuthCookie = res.cookies.get("siyuan")
    print(AuthCookie)


class Block:
    def __init__(self,
                 alias, box, content,
                 created, hash, ial, id, length,
                 markdown: str, memo, name,
                 next_id, parent_id, path,
                 previous_id, root_id, sort):
        self.alias = alias
        self.box = box
        self.content = content
        self.created = created
        self.hash = hash
        self.ial = ial
        self.id = id
        self.length = length
        self.markdown = markdown
        self.memo = memo
        self.name = name
        self.next_id = next_id
        self.parent_id = parent_id
        self.path = path
        self.previous_id = previous_id
        self.root_id = root_id
        self.sort = sort
        self.properties = parse_ial(self.ial)

    def __init__(self, dict):
        for x in dict:
            setattr(self, x, dict[x])
        self.properties = parse_ial(self.ial)


"""
BlockPool = {}
def get_block(dict) -> Block:
    ret = BlockPool.get(dict["id"])
    if ret is None:
        ret = Block(dict)
        BlockPool[dict["id"]] = ret
    return ret
"""


def query_sql(SQL: str):
    result = post(API_URL + "query/sql", stmt=SQL).json()
    if result["code"] == 0:
        return result["data"]
    raise ApiException(result)


class NullBlockException(Exception):
    pass


def find_by_id(id: str) -> Block:
    res = query_sql(r"SELECT * FROM blocks WHERE id='{}'".format(id))
    if len(res) <= 0:
        raise NullBlockException
    return Block(res[0])


def get_col_by_id(id: str, attr_name: str):
    # print("get_col_by_id", id, attr_name)
    res = query_sql(
        r"SELECT {} FROM blocks WHERE id='{}'".format(attr_name, id))
    if len(res) <= 0:
        raise NullBlockException
    return res[0][attr_name]


def get_property_by_id(id: str, property_name: str):
    ial = get_col_by_id(id, "ial")
    match = re.search(r" {}=\"(.+?)\"".format(property_name), ial)
    if match is None:
        raise Exception("Property Not Found.")
    return match.group(1)


def do_property_exist_by_id(id: str, property_name: str):
    # print(id)
    ial = get_col_by_id(id, "ial")
    return property_name in ial


def get_sons_by_id(id: str):
    return query_sql(r"SELECT id FROM blocks WHERE parent_id='{}'".format(id))


def get_parent_by_id(id: str):
    # print("get parent by id: {} parent: {}".format(
    # id, get_col_by_id(id, "parent_id")))
    return get_col_by_id(id, "parent_id")
