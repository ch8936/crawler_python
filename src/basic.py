# python 爬虫基础知识

一.爬虫基础

1.1 什么是爬虫
请求网站并提取数据的自动化程序。

1.2 爬虫的基本流程
①发起请求：
通过HTTP库向目标站点发起请求，即发送一个Request,请求可包含额外的headers等信息，等待服务器响应。
②获取响应内容：
如果服务器能正常响应，会得到一个Response,Response的内容便是所要获取的页面内容，类型可能有HTML,Json字符串，二进制数据（如图片视频）等类型。
③解析内容：
得到的内容可能是HTML，可用正则表达式、网页解析库进行解析。可能是Json,可直接转为Json对象解析，可能是二进制数据，可以保存或进一步处理。
④保存数据：
保存形式多样，可存为文本，也可保存至数据库，或者保存特定格式的文件。

1.3 Request的组成
①请求方式：
主要有GET、POST两种类型，另外还有HEAD、PUT、DELETE、OPTIONS等。
②请求URL：
UEL全称统一资源定位符，如一个网页文档、一张图片、一个视频等都可以用URL唯一来确定。
③请求头：
包含请求时的头部信息，如User-Agent、Host、Cookies等信息。
④请求体：
请求时额外携带的数据，如表单提交时的表单数据。

1.4 Response的组成
①响应状态：
200代表成功、301跳转、404找不到页面、502服务器错误
②响应头：
如内容类型、内容长度、服务器信息、设置Cookie等。
③响应体
最主要的部分，包含了请求资源的内容，如网页HTML、图片二进制数据等。

1.5 能抓怎样的数据？
①网页文本，如HTML文档，Json格式文本等
②图片，获取到的是二进制文件，保存为图片格式
③视频，同为二进制文件，保存为视频格式即可
④其他，只要是能请求到的，都能获取

1.6 解析方式
①Json
②正则表达式
③BeautifulSoup
④PyQuery
⑤XPath

1.7 怎样解决JavaScript渲染的问题？
①分析Ajax请求
②Selenium/WebDriver
③Splash
④PyV8、Ghost.py

1.8 怎样保存数据？
①文本：
如文本、Json、Xml等
②关系型数据库：
如MySQL、Oracle、SQL Server等具有结构化表结构形式存储
③非关系型数据库：
如MongoDB、Redis等Key-Value形式存储
④二进制文件：
如图片、视频、音频、等直接保存成特定格式即可。 


二.Urllib库详解

2.1 什么是Urllib？
Python内置的HTTP请求库
urllib.request       请求模块
urllib.error         异常处理模块
urllib.parse         url解析模块
urllib.robotparser   robots解析模块

2.2 相比Python2的变化
Python2
import urllib2
response = urllib2.urlopen('http://baidu.com')

Python3
import urllib.request
response = urllib.request .urlopen('http://baidu.com')

2.3 urlopen
urllib.request.urlopen(url,data=None,[timeout,]*,cafile=None,capath=None,cadefault=False,context=None)

import urllib.request
response = urllib.request.urlopen('http://baidu.com')
print(response.read().decode('utf-8'))

import urllib.request
import urllib.parse
data = bytes(urllib.parse.urlencode({'word':'hello'}),encoding='utf-8')
response = urllib.request.urlopen('http://httpbin.org/post',data = data)
print(response.read())

import urllib.request
response = urllib.request.urlopen('http://httpbin.org/get',timeout=1)
print(response.read())

import urllib.request
import urllib.error
import socket
try:
	response = urllib.request.urlopen('http://httpbin.org/get',timeout=0.1)
except urllib.error.URLError as e:
	if isinstance(e.reason,socket.timeout):
		print('TIME OUT')

2.4 响应
响应类型
import urllib.request
response = urllib.request.urlopen('http://www.python.org')
print(type(response))

状态码、响应头
import urllib.request
response = urllib.request.urlopen('http://www.python.org')
print(response.status)
print(response.getheaders())
print(response.getheader('Server'))

Request
import urllib.request
request = urllib.request.Request('http://www.python.org')
response = urllib.request.urlopen(request)
print(response.read().decode('utf-8'))


