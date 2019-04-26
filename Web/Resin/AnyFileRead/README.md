### 漏洞简介

默认下Resin的/webapps目录下/resin-doc中包含有一个扩展war文件。该文档包含有用于在集成的手册中浏览文件的servlet：
```
http://localhost/resin-doc/viewfile/?contextpath=%2Fresin-doc%2Fjmx%2Ftutorial%2Fbasic&servletpath=%2Findex.xtp&file=index.jsp&re-marker=&re-start=&re-end=#code-highlight
```

viewfile servlet可以无需参数在Web主目录中浏览任意文件：
```
http://localhost/resin-doc/viewfile/?file=index.jsp
```

请注意这句话：攻击者可以设置resin-doc外的上下文路径，读取其他Web主目录的任意文件

### 影响版本

Caucho Technology Resin v3.0.10 ~ v3.0.18

### 漏洞利用

见Poc