# popup-dict

Linux 下的划词翻译工具，支持使用有道等多种翻译服务。

使用 Python 3 + Gtk+ 3 编写，适用于 Gnome 桌面环境。

![screenshots](./screenshots/popup.png)

功能特点：

* 目前只支持英文->中文翻译
* 主要针对 Gnome 桌面环境，不保证其它环境下的正常使用
* 鼠标划词翻译，弹窗显示
* 智能处理选中内容（去除两端非英文字符、压缩空白字符、删除换行符等）
* 弹窗显示一段时间后自动关闭。若鼠标在弹窗中，延迟关闭
* 点击弹窗中链接可打开有道词典网页版

本工具主要受 [@idning](https://github.com/idning/) 的 [youdao-dict-for-ubuntu](https://github.com/idning/youdao-dict-for-ubuntu/) 启发。

## 依赖

* Python 3.5+
* Gtk+ 3
* [PyGObject](https://pygobject.readthedocs.io/en/stable/)
* Python packages:
    * [psutil](https://github.com/giampaolo/psutil)
    * [requests](https://github.com/requests/requests/)

## 安装

确保已安装 [PyGObject](https://pygobject.readthedocs.io/en/stable/getting_started.html)

__PyPI:__

```bash
sudo pip install popupdict
```

## 运行

```bash
popup-dict

# 查看帮助
popup-dict -h
```

可使用 Gnome Shell Extension [popup-dict-switcher](https://github.com/bianjp/popup-dict-switcher) 一键打开/关闭 `popup-dict`

## 配置

应用默认加载以下位置中第一个存在的配置文件：

* `~/.config/popup-dict/config.ini`
* `/etc/popup-dict/config.ini`

也可通过命令参数指定配置文件位置。

默认配置：

```ini
[global]
# 查询客户端
query_client = youdao-zhiyun
# 弹窗显示时间。单位：秒；类型：float
popup_timeout = 3
# 是否使用 Gtk Global Dark Theme。不设置或设为空则使用系统默认设置。类型: boolean
prefer_dark_theme=
# 调试模式
debug = false

# 适用于所有客户端的默认设置，可在各客户端的配置中覆盖
[client]
# 请求超时时间。单位：秒；类型：float
request_timeout = 3


##### 各客户端配置 ######

# 有道词典网页版
[youdao-web]

# 有道智云
# http://ai.youdao.com/doc.s#guide
[youdao-zhiyun]
app_id =
app_secret =
```

## Todo

* 实现有道词典网页版查询客户端
* 弹窗显示时自动发音
* 点击音标发音
* 根据选中文本位置而非鼠标位置定位弹窗（应对不用鼠标选中文本的情况；避免遮盖选中文本）
* 支持 Wayland
* 支持多显示器
* 展示某些错误提示（比如 API 授权错误）
* test
* 进程退出时删除 pid 文件
* 打包到 [AUR](https://aur.archlinux.org/)
* 版本更新提示

## 类似工具

GUI:

* https://github.com/idning/youdao-dict-for-ubuntu/
* https://github.com/FindHao/ciba
* https://github.com/jiffies/GouYong

Console:

* https://github.com/longcw/youdao
* https://github.com/felixonmars/ydcv
* https://github.com/farseerfc/ydcv-rs

## License

This project is licensed under the terms of the MIT license.
