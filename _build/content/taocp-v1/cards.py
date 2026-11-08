# -*- coding: utf-8 -*-
CARDS = [
{"id": "f01", "chapterId": "ch01", "front": "算法的五条准则是什么？", "back": "有限性、确定性、输入、输出、可行性。", "tags": ["定义"]},
{"id": "f02", "chapterId": "ch01", "front": "证明算法会停，要指出什么？", "back": "一个每轮严格减小、又有下界的量，例如欧几里得算法里的余数 r。", "tags": ["终止性"]},
{"id": "f03", "chapterId": "ch01", "front": "大 O 的严格定义是什么？", "back": "存在正常数 c 与 n₀，使所有 n ≥ n₀ 都有 f(n) ≤ c·g(n)。", "tags": ["复杂度"]},
{"id": "f04", "chapterId": "ch01", "front": "3n² + 5n + 7 = O(n²) 的依据是哪两个常数？", "back": "取 n₀ = 1、c = 15：5n ≤ 5n²、7 ≤ 7n²，整体不超过 15n²。", "tags": ["复杂度"]},

{"id": "f05", "chapterId": "ch02", "front": "数学归纳法的两步分别叫什么？", "back": "奠基（验证起点）与归纳（由 n 成立推出 n+1 成立）。", "tags": ["证明"]},
{"id": "f06", "chapterId": "ch02", "front": "等比求和的闭式是什么？", "back": "Σ(k=0 到 n) x^k = (1 − x^(n+1))/(1 − x)，x ≠ 1。", "tags": ["求和"]},
{"id": "f07", "chapterId": "ch02", "front": "C(n, k) 的帕斯卡递推怎么写？", "back": "C(n, k) = C(n−1, k−1) + C(n−1, k)。", "tags": ["组合数"]},
{"id": "f08", "chapterId": "ch02", "front": "生成函数把递推变成了什么？", "back": "一个关于 z 的代数方程，解出 G(z) 后展开，系数就是通项。", "tags": ["生成函数"]},

{"id": "f09", "chapterId": "ch03", "front": "MIX 的一个字由什么组成？", "back": "1 个符号位加 5 个字节，每个字节 6 位，取值 0 到 63。", "tags": ["MIX"]},
{"id": "f10", "chapterId": "ch03", "front": "一条 MIX 指令包含哪四样信息？", "back": "操作码、地址、变址、域。", "tags": ["MIX"]},
{"id": "f11", "chapterId": "ch03", "front": "MIX 子程序靠什么返回？嵌套调用要注意什么？", "back": "靠 J 寄存器存返回地址；嵌套调用要先把 J 存进内存（保存链接字）。", "tags": ["子程序"]},
{"id": "f12", "chapterId": "ch03", "front": "解释程序的三段循环是什么？", "back": "取指、译码、执行。", "tags": ["解释程序"]},

{"id": "f13", "chapterId": "ch04", "front": "在单链表 P 之后插入 Q 的两步是什么？顺序能反吗？", "back": "先 Q.LINK = P.LINK，再 P.LINK = Q；不能反，否则 P 原来的后继地址会被覆盖。", "tags": ["链表"]},
{"id": "f14", "chapterId": "ch04", "front": "双链表删除节点 Q 要改哪两条链？", "back": "Q.LLINK.RLINK = Q.RLINK；Q.RLINK.LLINK = Q.LLINK。", "tags": ["链表"]},
{"id": "f15", "chapterId": "ch04", "front": "队列用普通数组实现会出现什么问题？怎么解决？", "back": "假溢出：队首后移留下永久空位。用循环数组，判满条件 (rear+1) mod m = front。", "tags": ["队列"]},
{"id": "f16", "chapterId": "ch04", "front": "循环链表用一个指针能访问什么？", "back": "从尾指针可以同时到达尾部（它自己）与头部（它的 LINK），插入删除都不必从头遍历。", "tags": ["链表"]},

{"id": "f17", "chapterId": "ch05", "front": "n 个节点的树有多少条边？为什么？", "back": "n − 1 条；除根以外每个节点恰贡献一条连向父节点的边。", "tags": ["树"]},
{"id": "f18", "chapterId": "ch05", "front": "三种遍历的差别在哪一点？", "back": "访问根的时机：先序最先、中序中间、后序最后。", "tags": ["遍历"]},
{"id": "f19", "chapterId": "ch05", "front": "一般树怎么变成二叉树？", "back": "用左孩子—右兄弟：LCHILD 指第一个孩子，RSIB 指下一个兄弟。", "tags": ["表示"]},
{"id": "f20", "chapterId": "ch05", "front": "扩充二叉树的 E 与 I 有什么关系？", "back": "E = I + 2n，n 是内部节点数。", "tags": ["路径长度"]},
{"id": "f21", "chapterId": "ch05", "front": "引用计数与标记-清扫各怕什么？", "back": "引用计数怕环（互相指向永不归零）；标记-清扫怕暂停（要扫一遍才能回收）。", "tags": ["垃圾回收"]},
{"id": "f22", "chapterId": "ch05", "front": "边界标记的作用是什么？", "back": "在块头块尾各存大小，使释放时能 O(1) 找到物理相邻的前后块并合并。", "tags": ["存储管理"]},
{"id": "f23", "chapterId": "ch05", "front": "伙伴系统怎么找「伙伴」块？", "back": "地址与块大小做异或：伙伴地址 = 地址 XOR 长度。只有同尺寸的伙伴才能合并。", "tags": ["存储管理"]},
]
