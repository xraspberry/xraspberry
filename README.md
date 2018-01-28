# raspberry

something X🎩 in raspberry

Start
===

```bash
git clone https://github.com/Microndgt/xraspberry.git
cd xraspberry
pip install .
```

设置以下环境变量：

- `X_EMAIL_SERVER` (optional, default smtp.qq.com)
- `X_EMAIL_USERNAME`
- `X_EMAIL_PASSWORD`
- `X_LOG_LEVEL` (optional, default DEBUG)

Then have fun!

DONE
===

1. 邮件提醒

    ```python
   from xraspberry import send_email
   send_email(subject="", msg="")
    ```
   
   or
   
   ```bash
    python bin/send_email.py subject msg
   ```

2. 数据库迁移
    
    当前使用sqlite，为了存储将来可能会有的数据
    
    ```bash
    # 初始化数据库
    bin/db_init.sh
    # 创建迁移脚本
    bin/db_migrate.sh revision_msg
    # upgrade 数据库
    bin/db_upgrade.sh
    ```

3. web系统 using golang
    
    ```bash
    ln -sf raspberry/xraspberry/xweb to/your/go/path/src/xweb
    cd xweb
    go build
    ./web
    ```

TODO
===

1. 室内温度监测，邮件提醒和展示 - `[xtemperature]`
2. 监控视频(晚上睡觉监测😂) - `[xvideo]`
3. 每天进出门记录和提醒(兼有防盗功能) - `[xwelcome]`

xweb API
===

/
---

GET: Hello xraspberry

Golang安装和配置
===

- [下载地址](https://golang.org/dl/)
- [安装教程](https://golang.org/doc/install)