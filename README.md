# aigf-mvp
### 轻量化AI恋人应用最小化实现项目
This is a minimized implementation that eliminates the heavy configuration operations of SillyStarven, making it a more player friendly AI girlfriend application

人类历史上从未有哪个时代像现在这样，每天产生180亿条消息，却仍有3400万人正在经历持续性孤独。
我希望所有孤独的人都能有人陪伴
Never in human history has there been a time like now where 18 billion messages are generated every day, yet 34 million people are still experiencing persistent loneliness.
I hope that all lonely people can have someone to accompany them

## 使用前需要配置的 AI 服务（目前支持 9 种，可任选其一）

- 阿里云百炼（当前版本可以先不用）

  获取自己的 `api key`，地址戳这里 👉🏻 ：[阿里云百炼平台](https://bailian.console.aliyun.com/?tab=model#/api-key)  
  将获取到的`api key`填入 `settings.py` 文件中的 `DASHSCOPE_API_KEY` 中。

- 百度机器翻译

  先获取自己的 `api key`，地址戳这里 👉🏻 ：[创建你的 api key](https://fanyi-api.baidu.com/manage/developer)

  将获取到的`api key` 和 `app id` 分别填入 `settings.py` 文件中的 `BAIDU_APPKEY` 和 `BAIDU_APPID` 中。

- MiniMax
  
  先获取自己的 `group id`，地址戳这里 👉🏻 ：[获取你的 group id](https://platform.minimaxi.com/user-center/basic-information)

  先获取自己的 `api key`，地址戳这里 👉🏻 ：[创建你的 api key](https://platform.minimaxi.com/user-center/basic-information/interface-key)

  将获取到的`group id` 和 `api key` 分别填入 `settings.py` 文件中的 `MINIMAX_GROUP_ID` 和 `MINIMAX_API_KEY` 中。
  
- Huggingface Token(这一步需要VPN)
  
  先获取自己的 `token`，地址戳这里 👉🏻 ：[创建你的 token](https://huggingface.co/settings/tokens)

  将获取到的`token` 填入 `settings.py` 文件中的 `HUGGINGFACE_TOKEN` 中。

## 开发/使用

检查好自己的开发环境，确保已经安装了 `python 3.10` , 本人本地开发版本python 3.10.16.

1. Python安装与服务启动
conda的安装自行百度
> conda create -n aigf python=3.10.16 -y
> 
> conda activate aigf
> 
> mv settings_example.py settings.py (将前面申请的key全都填好)
> 
> cd aigf-mvp && pip install -r ./requirements.txt
> 
> python server.py
