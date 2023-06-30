# py_inscryption_advanced
对PyInscryption的套壳,更加友好，可以通过牌堆JSON的方式直接生成可打印PDF
## 在开始之前：
### 牌堆是什么？
牌堆是程序定义的一种描述需要的牌的方式，比如指定16张松鼠，1张白鼬，一张臭虫，一张狼崽，一张牛蛙\
它们会被按照顺序填充进PDF,然后你把它用打印机打出来，剪开，就是可以玩的卡了。\
牌堆的定义方式会在后面讲述。
### 贴花是什么？ (v0.0.2+)
贴花是卡牌最上层覆盖的一层（通常是半透明的）贴图，比如游戏中大白鲨表面的血渍，凯西MOD中的粘液等等，英文称之为Decal。
本程序包含了游戏中所有贴花，名字可自行在py_inscryption/builtin_resources/cards/decal处查找。
在卡牌.json配置文件中使用时，项为"decals",值为一个数组，包含贴花的名字(不包含decal_前缀和.png后缀)。
为了兼容v0.0.1创建的配置文件，该项是可选的。
### 印记
卡牌的额外能力，项为"abilities",值为一个数组，其中包含能力的名字(不包含abilitiy_前缀和.png后缀),名字可自行在py_inscryption/builtin_resources/abilities处查找。
### 献祭印记
在游戏中使用怪石献祭造物而附加在别的卡牌上的印记，呈蓝色。
项为"sacrisfied_abilities"，值的规则与"ability"相同。
为了兼容v0.0.1创建的配置文件，该项是可选的。
## 用法？
先启动一次`app.py`，退出。\
生成如下文件夹：\
cards - 存储卡牌数据以及造物贴图\
 |- textures - 存储造物贴图\
 |- *.json - 由用户创建，定义一张卡牌\
decks - 存储用户自定义的牌堆\
 |- *.json 由用户创建，定义一个牌堆\
generated_cards - 存储程序自动创建的卡牌图片和背面\
 |- 不用管它\
output - 存储最终的可打印PDF,来自于牌堆\
 |- *.pdf 生成的结果\
我们先定义一张卡牌吧：\
在cards目录下创建一个文件：`squirrel.json`\
内容填什么好呢？
```
{
    "front": "",
    "back": "squirrel",
    "beast": "squirrel.png",
    "name": "松鼠",
    "damage": 0,
    "health": 1,
    "cost_type": "blood",
    "cost": 0,
    "abilities":[]
}
```
它们的含义应该清晰明了。\
有这几个需要注意的点：\
"front","back"与"abilities"分别代表卡牌的正面底座,背面和能力，它们的名字在py_inscryption/builtin_resources里找到。程序会自动帮你加上前缀。\
"cost_type"可为"blood"或"bone",上限分别为4与10，因为游戏的资源文件里最大只有这个......\
"beast"指定的造物材质要扔到"cards/textures/"里\
这样我们就有了松鼠牌的模板\
然后我们定义牌堆：\
在decks目录下创建一个文件： `more_squirrels.json`\
因为要更多松鼠，所以嘻嘻：
```
{
    "deck": [
        ["squirrel",41]
    ]
}
```
用一个数组来指定特定数量的牌，再把这个数组塞到"deck"里。名字就是cards目录下卡牌文件的名字。\
这样一个包含41张松鼠牌的牌堆就完成了。\
运行`app.py`输入牌堆的名字，去`output`中找到pdf,把它打出来吧，awa。

