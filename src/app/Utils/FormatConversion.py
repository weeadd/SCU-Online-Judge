import json
import pandas as pd

# 数据库结果转json工具函数
def toJSON(res):
    # 获取查询结果的列名
    keys = res.keys()

    # 将 ResultProxy 对象转换为字典列表
    results = [dict(zip(keys, row)) for row in res]

    # 将字典列表转换为 JSON
    json_results = json.dumps(results)

    return json_results

def toDataFrame(res):
    data = [row._asdict() for row in res]
    df = pd.DataFrame(data)
    return df