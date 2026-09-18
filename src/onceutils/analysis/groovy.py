from os import PathLike
from pathlib import Path
from typing import List, Optional, Union


class GroovyBlock:
    """Groovy 脚本中的一个块，对应源码里的 ``name { ... }``。

    块树由 GroovyScript.parse() 构建。children 是直接子块，顺序与源码一致；
    匿名块（如 ``{ ... }`` 闭包字面量）的 name 是空字符串。

    位置字段（由 parse 注入，构造后只读）：
    - start: name 起点；匿名块时等于 body_start
    - body_start: '{' 的位置
    - end: '}' 之后的位置（切片上界）

    取文本用 :attr:`text`（含 name）或 :attr:`content`（不含 name，从 '{' 起）。
    """

    def __init__(self, name: str):
        self.name = name
        self.start: int = 0         # name 起点（匿名块时等于 body_start）
        self.body_start: int = 0    # '{' 位置
        self.end: int = 0           # '}' 之后（切片上界）
        self._source: str = ""      # 原始文本（parse 注入，供 text/content 切片）
        self.children: List[GroovyBlock] = []

    def find(self, name: str, deep:bool=True) -> "Optional[GroovyBlock]":
        if deep:
            return self._deep_find(name)
        for child in self.children:
            if child.name == name:
                return child

    def _deep_find(self, name: str) -> "Optional[GroovyBlock]":
        """在后代中查找第一个名为 name 的块，找不到返回 None（不检查自身）。

        "第一个"指源码里先出现的那个。以这棵树为例（children 按源码顺序）::

            root
            ├── a          <- children[0]
            │   ├── d
            │   ├── e
            │   └── f
            ├── b
            └── c          <- children[-1]

        三种写法的栈内容逐步变化（栈底在左；"出 a" 这行是出栈 a 之后的栈）::

            出栈    实现一          实现二          实现三
                    reversed + pop  不 reversed     pop(0) 队列
            --------------------------------------------------
            初始    [c b a]         [a b c]         [a b c]
            a       [c b f e d]     [a b]           [b c d e f]
            d       [c b f e]       [a]             [c d e f]
            e       [c b f]         [d e f]         [d e f]
            f       [c b]           [d e]           [e f]
            b       [c]             [d]             [f]
            c       []              []              []
            访问    a d e f b c     c b a f e d     a b c d e f

        三种都是遍历方式，特点不同、按需来选：
        实现一（深度优先前序）：读完 a 的整棵子树再读兄弟 b、c，等于源码里从上
                                往下读，先命中源码里最靠前的同名块；
        实现二（深度优先前序，子块倒序取）：先读 c、b，进 a 后又从 f 读到 d，
                                先命中源码里最靠后的同名块；
        实现三（广度优先）：先把浅层的 a、b、c 都读完再进下一层，先命中层数最
                                浅的同名块，同层仍按源码顺序。

        find() 要的是"源码里第一个"，所以取实现一。

        用显式栈而非递归：树深由输入文件决定，递归会撞 Python 的递归上限
        （畸形或机器生成的脚本可能有上千层嵌套），显式栈在堆上，不受此限。
        """
        # 逆序压入，children[0] 才会第一个出栈；三种写法的对比见 docstring
        stack = list(reversed(self.children))
        while stack:
            block = stack.pop()
            if block.name == name:
                return block
            # 同样逆序，让子块先于栈里等着的兄弟节点被访问，即深度优先
            stack.extend(reversed(block.children))
        return None

    @property
    def text(self) -> str:
        """包含 name 的整块文本：``name { ... }``，从 start 到 end。"""
        return self._source[self.start:self.end]

    @property
    def content(self) -> str:
        """不含 name 的内容：从 ``{`` 起到 ``}`` 结束，含两侧花括号。"""
        return self._source[self.body_start:self.end]

    @property
    def child_names(self) -> List[str]:
        """直接子块的名字，按源码顺序；不含更深层（要跨层找请用 find）。"""
        return [child.name for child in self.children]

    def __repr__(self) -> str:
        return f"GroovyBlock({self.name!r}, {len(self.children)} children)"


class GroovyScript:
    """一份 Groovy 脚本的轻量词法 + 语法分析：按成对的 '{' / '}' 构建块树。

    只认 Groovy 语法本身，不解释任何 DSL 语义 —— Gradle、AGP 的概念
    （productFlavors、buildTypes …）由调用方自己解释。

    用法::

        script = GroovyScript(Path("app/build.gradle"))   # 构造即读文件并解析
        script.block("android").find("buildTypes")        # 任意深度的块都能查
        script.root.child_names                           # 顶层块名
    """

    def __init__(self, path_build: Union[str, PathLike]):
        """构造即读取并解析该文件；路径不存在会直接抛 FileNotFoundError。"""
        self.path = Path(path_build)
        self.root = self.parse(self.path.read_text(encoding="utf-8"))

    # ---------------- 解析 ----------------

    @staticmethod
    def parse(text: str) -> GroovyBlock:
        """把 Groovy 脚本文本解析成块树，返回 name 为空串的根块（根不参与匹配）。

            单次扫描同时做两层：
            - 词法：注释与字符串字面量整体跳过，它们内部的 '{' / '}' 不参与配对；
            - 语法：用栈匹配成对的 '{' / '}'，把紧邻 '{' 的标识符当作块名。

            例：``android { productFlavors { free { } } }`` 得到一条链
            root → android → productFlavors → free；
            而注释 ``// a {`` 和字符串 ``"b {"`` 里的 '{' 不建块（词法层已跳过）。

            括号不平衡不报错，按已有结构收尾：多余的 '}' 忽略，未闭合的块保持打开。

            每个块带三个位置标记（构造后只读）：
            - start: name 起点；``block.text`` 拿到 ``name { ... }``
            - body_start: '{' 位置；``block.content`` 拿到 ``{ ... }``
            - end: '}' 之后的位置（切片上界）
            """
        root = GroovyBlock("")
        root._source = text           # 整棵树共享同一份文本，避免每块都存
        root.start = root.body_start = 0
        root.end = len(text)
        stack = [root]                # 栈顶是当前正在收集子块的节点
        buf = ""                      # 正在累积的标识符
        pending = ""                  # 最近读完的标识符，供 `name {` 这种带空白的取名
        i = 0
        n = len(text)

        while i < n:
            ch = text[i]

            # ---- 词法：跳过注释 ----
            if text.startswith("//", i):
                j = text.find("\n", i)
                i = n if j < 0 else j
                buf = pending = ""
                continue
            if text.startswith("/*", i):
                j = text.find("*/", i + 2)
                i = n if j < 0 else j + 2
                buf = pending = ""
                continue

            # ---- 词法：跳过字符串字面量（含三引号与反斜杠转义）----
            if ch == '"' or ch == "'":
                triple = text.startswith(ch * 3, i)
                quote = ch * 3 if triple else ch
                j = i + len(quote)
                while j < n:
                    if not triple and text[j] == "\\":
                        j += 2
                        continue
                    if text.startswith(quote, j):
                        j += len(quote)
                        break
                    j += 1
                i = j
                buf = pending = ""
                continue

            # ---- 语法：'{' 压栈开块，紧邻的标识符就是块名 ----
            if ch == "{":
                name = buf or pending
                # 从 '{' 倒推 name 起点：跳过 name 与 '{' 之间的空白
                k = i - 1
                while k >= 0 and text[k].isspace():
                    k -= 1
                block_start = max(0, k - len(name) + 1) if name else i
                block = GroovyBlock(name)
                block._source = text
                block.start = block_start
                block.body_start = i                  # '{' 位置
                stack[-1].children.append(block)
                stack.append(block)
                buf = pending = ""
                i += 1
                continue

            # ---- 语法：'}' 弹栈闭块 ----
            if ch == "}":
                if len(stack) > 1:    # 多余的 '}' 直接忽略，不破坏已建好的结构
                    stack[-1].end = i + 1             # '}' 之后作为切片上界
                    stack.pop()
                buf = pending = ""
                i += 1
                continue

            # ---- 词法：标识符字符 ----
            if ch.isalnum() or ch == "_":
                buf += ch
                i += 1
                continue

            # ---- 空白只是结束标识符；其它符号（. ( ) : , = -> …）一律断开 ----
            if ch.isspace():
                if buf:               # 空白结束标识符，先记进 pending，后面的 '{' 可能要用
                    pending, buf = buf, ""
            else:
                buf = pending = ""
            i += 1

        return root

    # ---------------- 查询 ----------------

    def block(self, name: str) -> Optional[GroovyBlock]:
        """从根开始跨层查找名为 name 的块（命中顺序同 GroovyBlock.find）。"""
        return self.root.find(name)
