# 交大主图书馆小组讨论室借用脚本

## 1. 脚本功能

交大图书馆讨论室可以由三个学生组队借用，其中第一个学生发起申请，后两(多)个学生凭单号和密码加入。

本脚本通过使用Cookie避免了多次登陆和点击的烦恼，你唯一需要做的就是获取**自己以及其他两位同学**登录[讨论室借用网站](http://studyroom.lib.sjtu.edu.cn/index.asp)后的Cookie之一**JASiteCookies**，将其添加到脚本的第29行的列表当中。

注意：如果您使用我代码中的三行Cookie借到讨论室，您仍然无法通过刷校园卡进入该讨论室。

## 2. Cookie获取方式

1. 添加Chrome插件[EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg)
2. 登录到上述网页后点击chrome右上角的小饼干图标
3. 将最后一项 -- JASiteCookies点开，那一长串的字符就是我们需要的Cookie啦

## 3. 使用建议

1. 请勿多次测试此脚本，测试后请及时在上述借用网站退掉不使用的讨论室
2. 请遵守[讨论室借用规范](http://studyroom.lib.sjtu.edu.cn/rule.asp)

## 4. 使用帮助

``` python main.py -h```

例如：

1. 借用明天晚上八点开始的E310房间，持续时长默认为4小时

   ``` python main.py -d tomorrow -s 20 -r E310 ```

   ``` python main.py -d 1 -s 20 -r E310 ```	ps: 这里date参数如果使用数字，则表示从今天开始的第几天

2. 借用下个星期五早上十点开始的任何房间，持续时长默认为4小时

   ```python main.py -d Fri -s 10```

3. 借用此时此刻接下来的任何讨论室2小时

   ```python main.py -l 2```

