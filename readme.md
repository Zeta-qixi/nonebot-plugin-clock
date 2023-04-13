# ⏰ | 提醒事项  支持群聊或私聊

## 配置文件设置
```
CLOCK_WHITE_LIST = [qq_id1, qq_id2, ...] 
CLOCK_BLACK_LIST = [qq_id] 
```
判定逻辑:
1. superuser 永远为`True`
2. 判定黑名单 启用后 用户在黑名单中直接返回`False`（高于 管理员 群主 权限）
3. 判定白名单 启用后 普通群员不在白名单中返回`False`（低于 管理员 群主 权限）


## __使用__

## 添加
> 添加闹钟 22:00 睡觉啦  
> bot : ...  
> y
```
user : [添加闹钟|设置闹钟|addclock] TIME NOTE
bot（询问类型） : 不重复, 设置为每日输入[Y/y], 设置自定 如周一周三输入[13]
user : [types]

- time 闹钟时间, 格式 H:M(24时制)  或 +30M , +1H （类似倒计时）
- note(可选) 可以输入@ ,图片, 视频等
- types

    - Y / y  设置为每天重复
    - 输入数字则设置为对应星期的**重复**。 周一周三 13,  1234567 = y
    - 输入 m.d 设定在m月d日单次**不重复**, 圣诞节 12.25
    - 输入其他 设定不重复
    
```


## 查看
> 查看闹钟｜提醒事项


## 删除
> 删除闹钟 4
```
删除闹钟 ID
    - ID 闹钟对应id (`查看闹钟`第一项)
```



## 更新
- 2023.4.12  优化⏰ [issues #1](https://github.com/Zeta-qixi/nonebot-plugin-clock/issues/1)
- 2023.4.13  优化⏰ [issues #1](https://github.com/Zeta-qixi/nonebot-plugin-clock/issues/1) 优化⏰ [issues #2](https://github.com/Zeta-qixi/nonebot-plugin-clock/issues/2)