# sliding_puzzle

## 设计思路

主要程序被拆分为三个部分

- main.py 主要负责游戏显示和用户交互
- engine.py 主要负责后端的状态更新以及约束验证
- solver.py 主要负责解法的运算

设计思路主要使用两个单例(GameEngine 和 Solver)，分别作为模拟器和计算器

游戏的 GUI 使用 pygame 实现 \
https://www.pygame.org/docs/

其中为了保证搜索的效率，solver 采用双向 BFS 实现 \
https://www.geeksforgeeks.org/bidirectional-search/

其中涉及的状态压缩(见 Solver.getHash)的算法为康拓展开 \
https://zh.wikipedia.org/wiki/%E5%BA%B7%E6%89%98%E5%B1%95%E5%BC%80

## 使用说明

在运行之前先安装必备 python 库

```bash
pip install -r requirements.txt
```

可以直接使用 python 调用 main.py 运行

```bash
python main.py \
--board_size=3 \
--random_step=20 \
--input_puzzle=input_puzzle.txt
```

将命令行在文件夹根目录运行

```bash
bash play_game.sh
```

也可以直接使用 python

可以调整的参数包括

- board_size 如果是自己玩，可以任意设置 3-10 任意尺寸，如果需要调用 solve，建议设置为<=5 的数，否则运算量超出极限
- random_step 打乱的步数，默认为 20，可以不用动这个参数
- input_puzzle 如需输入给定的初始局面，在对应 txt 文件中按照 input_puzzle.txt 格式输入即可

![game sample](./sample.png)

游戏操作

- 游戏中任意时刻，可点击 New Game，打乱拼图开始新的游戏
- 游戏中任意时刻，可点击 Solve，可以让程序自动开始解决剩余步数，界面左上角显示"Automatically Solving..."
- 当胜利时，界面左上角显示"You WIN!"
