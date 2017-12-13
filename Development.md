# 开发

```bash
# 以开发模式安装本包
# 可能需要 root 权限
python setup.py develop

# 运行
popup-dict

# 卸载
python setup.py develop --uninstall
```

## 设计目标

* 使用 Gnome 原生方式（Gtk+ 3）
* 响应快（主线程不能阻塞）
* 界面好看
* 方便扩展支持其它翻译服务

## 注意事项

* Gtk+ 3 非线程安全，因此只在主线程中渲染 UI
* 主线程中不能有阻塞的操作（如 `time.sleep`, HTTP 请求等）

## 技术难题

* 支持翻译其它语言

  文本过短时难以准确识别语言（某些语言共用部分字符），而部分翻译服务要求指定源语言（如有道网页版）

* 进程退出时删除 pid 文件

  尚未找到可靠的方式在进程收到 signal 时执行代码
