# 开发

## 设计目标

* 优先使用 Gnome 原生/自带组件（Gtk+ 3, GStreamer）
* 系统依赖少（PyPI 包可以例外）
* 响应快（主线程不能阻塞或过于繁忙）
* 界面好看
* 方便扩展支持其它翻译服务

## 开发环境

```bash
# 安装依赖
sudo pip install -r requirements.txt

# 以开发模式安装本包
# 可能需要 root 权限
sudo python setup.py develop

# 运行
popup-dict

# 卸载
sudo python setup.py develop --uninstall
```

## 发布流程

1. 更改版本号: `popupdict/__init__.py`
2. 添加更新日志
3. 提交代码，并打标签: `git tag v0.1`
4. 确保工作目录干净，以免打包时把未提交的内容包含进去

__发布到 TestPyPI:__

正式发布到 [PyPI](https://pypi.org) 前，应先发布到 [TestPyPI](https://test.pypi.org/) 测试

[Setting up TestPyPI in pypirc](https://packaging.python.org/guides/using-testpypi/#setting-up-testpypi-in-pypirc)

```bash
rm -rf dist/*
python setup.py sdist bdist_wheel
twine upload -r testpypi dist/*
```

__发布到 PyPI：__

```bash
rm -rf dist/*
python setup.py sdist bdist_wheel
twine upload dist/*
```

## 增加查询客户端

1. 继承 `AbstractQueryClient`，实现查询类
2. 如果需要额外的配置项，增加配置类（继承 `ClientConfiguration`），并在 `popupdict/config/default.ini` 中添加默认配置
3. 将查询类添加到 `popupdict/query/client/__init__.py` 中的 `valid_clients`

## 注意事项

* Gtk+ 3 非线程安全，因此只在主线程中渲染 UI
* 主线程中不能有阻塞的操作（如 `time.sleep`, HTTP 请求等）

## 技术难题

* 支持翻译其它语言

  文本过短时难以准确识别语言（某些语言共用部分字符），而部分翻译服务要求指定源语言（如有道网页版）

* 进程退出时删除 pid 文件

  尚未找到可靠的方式在进程收到 signal 时执行代码

* 动词的单三、进行时、过去式等形式，名字的复数形式，转为原始形式再查询，以获得更好的查询结果

## 参考资料

* [Python GTK+3 Tutorial](https://python-gtk-3-tutorial.readthedocs.io/en/latest/)
* [PyGObject API Reference](https://lazka.github.io/pgi-docs/)
* [GTK+3 Source Code](https://github.com/GNOME/gtk/)
* [PyGObject - Threading & Concurrency](https://pygobject.readthedocs.io/en/latest/guide/threading.html)
* [Wayland support in GTK+](https://wiki.gnome.org/Initiatives/Wayland/GTK%2B)
* [Gnome useful tools](https://wiki.gnome.org/Newcomers/SolveProject#Other_useful_tools)
* [GStreamer documentation](https://gstreamer.freedesktop.org/documentation/)
* [playbin design](https://gstreamer.freedesktop.org/documentation/design/playbin.html)
* [playbin usage](https://gstreamer.freedesktop.org/documentation/tutorials/playback/playbin-usage.html)
