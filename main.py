

import hashlib
import random
import requests
import time


appID = '20210519000833325'
secretKey = '_jt1WVvWNN88G_zXhafM'
apiURL = 'http://api.fanyi.baidu.com/api/trans/vip/translate'


def baiduAPI_translate(query_str, to_lang):
    # 生成随机的 salt 值
    salt = str(random.randint(32768, 65536))
    # 准备计算 sign 值需要的字符串
    pre_sign = appID + query_str + salt + secretKey
    # 计算 md5 生成 sign
    sign = hashlib.md5(pre_sign.encode()).hexdigest()
    # 请求 apiURL 所有需要的参数
    params = {
        'q': query_str,
        'from': 'auto',
        'to': to_lang,
        'appid': appID,
        'salt':salt,
        'sign': sign
    }
    try:
        # 直接将 params 和 apiURL 一起传入 requests.get() 函数
        response = requests.get(apiURL, params=params)
        # 获取返回的 json 数据
        result_dict = response.json()
        # 得到的结果正常则 return
        if 'trans_result' in result_dict:
            return result_dict
        else:
            print('Some errors', result_dict)
    except Exception as e:
        print('Some errors', e)


def baiduAPI_translate_main(query_str, dst_lang=''):
    if dst_lang:
        result_dict = baiduAPI_translate(query_str, dst_lang)
    else:
        result_dict = baiduAPI_translate(query_str, 'zh')
        if result_dict['from'] == 'zh':
            result_dict = baiduAPI_translate(query_str, 'en')
    dst = result_dict['trans_result'][0]['dst']
    return dst


if __name__ == '__main__':

    with open('output.txt', 'w', encoding='UTF-8') as ouput:
        ouput.truncate()   #清空文件

    with open('input.txt','r', encoding='UTF-8') as input:
        line = input.readline()

        while line:

            if line.strip() == "" :
                line = input.readline()
                with open('output.txt', 'a') as ouput:
                    ouput.write('\n')
                continue
            print(line)
            ans = baiduAPI_translate_main(line, 'en') # 这里调节参数选择中间层语言
            time.sleep(1)
            ans = baiduAPI_translate_main(ans, 'zh')
            time.sleep(1)
            print(ans)
            line = input.readline()