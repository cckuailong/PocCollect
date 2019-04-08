# D-Link service.cgi远程命令执行

## 简介

D-Link DIR 615/645/815路由器1.03及之前的固件版本存在远程命令执行漏洞。该漏洞是由于service.cgi中拼接了HTTP POST请求中的数据，造成后台命令拼接，导致可执行任意命令。

## 影响版本

D-Link DIR 615
D-Link DIR 645
D-Link DIR 815

## 漏洞复现

使用网络空间搜索引擎：ZoomEye

搜索表达式：app:"D-Link DIR-645 WAP http config"

使用POC进行攻击。