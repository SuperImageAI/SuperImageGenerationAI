# -*- coding: utf-8 -*-
"""
 @FileName: run_config.py
Created on 2019/6/21 11:16 by lxg

"""
import datetime
import hashlib
import copy


def get_data_digest(input_dict):
    """
    对输入字典的key按照降序排序，然后依次取出排序后的key对应的value值拼接成字符串，最后对字符串进行md5签名；
    :param input_dict:
    :return:
    """
    key_list = sorted(list(input_dict.keys()), reverse=True)  # 对key降序排列
    value_list = [input_dict[key] for key in key_list]
    value_str = "".join(value_list)
    m = hashlib.md5()
    m.update(value_str.encode("utf-8"))
    data_digest = m.hexdigest()
    return data_digest.upper()


def tf_sign(sign_dict, dog_ak, dog_sk):
    """
    请求对参加添加签名信息
    :param sign_dict: 调用第三方服务需要的参数
    :param dog_ak: 聚宝盆服务的accessKey
    :param dog_sk: 聚宝盆服务的securityKey
    :return: sign_dict添加时间戳、dog_ak、签名之后的dict转化成的json
    """
    info_dict = copy.deepcopy(sign_dict)
    time_stamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    info_dict.setdefault("tf_timestamp", time_stamp)
    info_dict.setdefault("dog_ak", dog_ak)
    info_dict.setdefault("dog_sk", dog_sk)
    sign = get_data_digest(info_dict)
    info_dict.setdefault("tf_sign", sign)
    del info_dict["dog_sk"]
    return info_dict


def lyt_url_sign(img_url, dog_ak, dog_sk):
    """对陆运通回单图片url进行加签（否则无法读取图片）"""
    doggy_url = img_url.split("/")[-1].split(".")[0]
    params_dict = {"doggyurl": doggy_url}
    signed_url = tf_sign(params_dict, dog_ak=dog_ak, dog_sk=dog_sk)
    seg_str_list = [img_url, "?", "doggyurl=", doggy_url, "&dog_ak=", dog_ak, "&tf_sign=",
                    signed_url["tf_sign"], "&tf_timestamp=", signed_url["tf_timestamp"]]
    result = "".join(seg_str_list)
    return result


run_config = dict(
    {
        "connection_list": [
            ("55Cf3455oe6989Z5", "XLH67Wd6wm458z5Zl8c8"),  # 聚宝盆  测试
            # ("2g993X712VUO7tX8", "6nOna09Ek4Ot78mh5GE8"),  # 聚宝盆 生产
        ],
        "confidence": 0,
        "receipt": "http://web-keyStoreWeb-vip/keyStoreWeb/thirdApi/baidubce/ocr/receipt",  # 聚宝盆-百度通用票据接口
        "general": "http://web-keyStoreWeb-vip/keyStoreWeb/thirdApi/baidubce/ocr/general_basic",  # 聚宝盆-百度通用文字接口
    }
)


xf_config = dict(
    {
        "connection_list": [
            ("55Cf3455oe6989Z5", "XLH67Wd6wm458z5Zl8c8"),  # 聚宝盆 测试
            # ("2g993X712VUO7tX8", "6nOna09Ek4Ot78mh5GE8"),  # 聚宝盆 生产
        ],
        "confidence": 0,
        "hand_write": "http://web-keyStoreWeb-vip/keyStoreWeb/thirdApi/iflytekOcr/handwriting",  # 聚宝盆-讯飞手写识别接口
        "general": "http://web-keyStoreWeb-vip/keyStoreWeb/thirdApi/baidubce/ocr/general_basic",  # 聚宝盆-百度通用文字接口
    }
)

url_sign_key = dict({
        "ak": "KlYSs650gUb86X83",  # 生产
        "sk": "w9q85320e1y3I7B36320"
    }
)

# img_audit_url = "http://10.51.40.105:19016/models/img_classify/"  # 测试
img_audit_url = "http://10.33.8.74:19016/models/img_classify/"  # 生产
# url_sign_key = dict({
#         "ak": "03ZG8msubj0n3829",  # 测试
#         "sk": "B3905K5x6ut3X73k9R78"
#     }
# )


IMG_RESIZE = 800  # 图片resize短边长度限制

# 运行日志（非logging模块所写日志）保存时长(天)
log_keep_time = 365

