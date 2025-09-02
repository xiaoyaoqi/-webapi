import requests
import json
from 登录 import post_request  # 导入登录模块

# 登录并获取会话信息
login_result = post_request()
if "error" in login_result:
    print("登录失败:", login_result["error"])
    exit()

cookies = login_result.get("cookies", {})
if not cookies:
    print("未获取到会话信息，请检查登录接口")
    exit()

# 金蝶 WebAPI 接口地址
url = "http://localhost/k3cloud/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.ExecuteBillQuery.common.kdsvc"

# 请求头
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# 请求参数
payload = {
    "parameters": [
        {
            "FormId": "PUR_PurchaseOrder",  # 表单标识
            "TopRowCount": 0,              # 返回的最大行数
            "Limit": 10,                   # 限制返回的记录数
            "StartRow": 0,                 # 起始行
            "FilterString": "FDocumentStatus = 'A'",  # 过滤条件
            "OrderString": "FID DESC",     # 排序规则
            "FieldKeys": "FID,FBillNo,FPOOrderEntry_FEntryID,FSrcBillNo,FDEMANDBILLNO"  # 返回字段
        }
    ]
}

# 发送 POST 请求
try:
    response = requests.post(url, headers=headers, cookies=cookies, data=json.dumps(payload))
    response.raise_for_status()  # 检查请求是否成功
    result = response.json()    # 解析响应为 JSON
    print("查询结果:", json.dumps(result, indent=4, ensure_ascii=False))
except requests.exceptions.RequestException as e:
    print("请求失败:", e)
