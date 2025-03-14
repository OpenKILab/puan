# puan
## 外部API接入
1. 在 /model 下新建 http_xxxapi_model.py
   1. 建议generate函数进行单独测试;
   2. 流式返回需要在parse中特殊处理;
2. 在puan_bot.py中导入 xxxAPI，并修改 model_cls = xxxAPI
## 流量控制
修改 post_url_task.py 中multi_lora_post_url任务的rate_limit
## 任务启动
### 请求队列启动
   1. 【linux/macos】celery -A post_url_task worker --loglevel=info --purge
   2. 【windows】celery -A post_url_task worker --loglevel=info --purge --pool=solo
注意: API不稳定，可以尝试设置--pool=solo
### 任务发放
python puan_bot.py