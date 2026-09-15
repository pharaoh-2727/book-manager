# 导入 os 模块：用于判断数据文件 books.json 是否存在
import os
# 导入 json 模块：用于图书数据的序列化（保存）与反序列化（加载）
import json

DATA_FILE = "books.json"

# ==================== 图书实体类 ====================
# 定义 Book 类：描述一本书的四个属性（书名、作者、年份、价格）
class Book:
    # 构造方法：创建 Book 实例时为四个属性赋值
    def __init__(self,title,author,year,price):
        self.title = title                                      # 书名
        self.author = author                                    # 作者
        self.year = year                                        # 出版年份
        self.price = price                                      # 价格
    # 定义对象的字符串表示：print(书籍对象) 时输出的内容
    def __str__(self):
        # 用 f-string 把四个属性拼成一行可读的书籍信息
        return f"《{self.title}》 | 作者：{self.author} | 年份：{self.year} | 价格：{self.price}元"
    # 修改价格：仅在传入值不为 None 时才更新
    def update_price(self,price):
        # 判断新价格是否为 None（None 表示「不修改」）
        if price is not None:
            self.price = price                                  # 覆盖实例的价格属性

# ==================== 工具函数 ====================
# 读取年份和价格：循环输入直到拿到两个合法数字才返回
# 单独抽成函数，是为了让 add_book 里不用再写一遍校验逻辑
def input_year_price():
    # 无限循环：输入不合法就一直重试，直到 return 才跳出
    while True:
        try:
            # 读取年份并转成整数（输入非数字会抛 ValueError）
            year = int(input("请输入年份："))
            # 读取价格并转成浮点数（价格可能有小数，所以用 float 而不是 int）
            price = float(input("请输入价格："))
            # 数字格式对了还不够，还要检查取值范围是否合理
            if year <= 0 or price < 0:
                # 提示哪里不对
                print("年份要大于 0，价格不能为负，请重新输入")
                # 跳过本轮剩余代码，回到循环开头重新输入
                continue
            # 格式和范围都合法才返回；返回的是元组，调用处可解包成两个变量
            return year, price
        # int() 或 float() 转换失败（用户输入的不是数字）
        except ValueError:
            # 提示并进入下一轮循环
            print("年份和价格必须是数字，请重新输入")


# ==================== 图书馆管理类 ====================
# 定义 Library 类：封装图书的增删改查与数据存取
class Library:
    # 构造方法：初始化一个空列表作为「书架」
    def __init__(self):
        self.books = []                                         # 存放所有 Book 对象
    # 添加图书：读取键盘输入，查重通过后追加到书架
    def add_book(self):
        # 读取书名；strip() 去掉首尾空格，避免「三体 」和「三体」被当成两本不同的书
        title = input("请输入书名：").strip()
        # 读取作者，同样去掉首尾空格
        author = input("请输入作者：").strip()
        # 遍历书架，检查这本书是否已经存在
        for book in self.books:
            # 书名和作者都相同才算重复（同名但不同作者的书允许共存）
            if book.title == title and book.author == author:
                # 提示已存在
                print(f"《{title}》（{author}）已存在")
                # 直接结束方法，不再往下录入
                return
        # 确认不重复后，才调用函数读取年份和价格，并解包成两个变量
        year, price = input_year_price()
        # 用四个信息创建一本 Book 对象，追加进书架列表
        self.books.append(Book(title, author, year, price))
        # 打印添加成功提示
        print(f"《{title}》已添加")
    # 修改价格：按书名+作者查找并更新价格
    def update_book(self):
        # 读取书名和作者，与 add_book 的查重标准保持一致
        title = input("请输入书名：").strip()
        author = input("请输入作者：").strip()
        # 遍历书架查找匹配的图书
        for book in self.books:
            # 书名和作者都对上才操作，避免误改同名的其他书
            if book.title == title and book.author == author:
                try:
                    # 读取新价格，输入非数字会抛出 ValueError
                    new_price = float(input("请输入新的价格："))
                # 输入非数字（如 abc），转换失败
                except ValueError:
                    # 提示并放弃本次修改
                    print("价格必须是数字，已取消修改")
                    # 直接结束方法，不继续往下走
                    return
                # 价格不能为负数
                if new_price < 0:
                    # 提示并放弃本次修改
                    print("价格不能为负数，已取消修改")
                    # 直接结束方法
                    return
                # 调用 Book 对象的方法，把新价格写进该对象
                book.update_price(new_price)
                # 打印修改结果
                print(f"《{title}》（{author}）的价格已更新为：{new_price}元")
                # 结束方法
                return
        # 循环走完仍未 return，说明没有匹配的书
        print(f"《{title}》（{author}）不存在")
    # 删除图书：按书名+作者查找并从书架移除
    def del_book(self):
        # 读取书名和作者，与 add_book 的查重标准保持一致
        title = input("请输入书名：").strip()
        author = input("请输入作者：").strip()
        # 遍历书架查找匹配的图书
        for book in self.books:
            # 书名和作者都对上才操作，避免误删同名的其他书
            if book.title == title and book.author == author:
                # 从列表中移除该 Book 对象（移除后立即 return，避免遍历中修改列表）
                self.books.remove(book)
                # 打印删除结果
                print(f"《{title}》（{author}）已删除")
                # 结束方法
                return
        # 循环走完仍未 return，说明没有匹配的书
        print(f"《{title}》（{author}）不存在")
    # 搜索图书：按书名查找并打印
    def search_book(self):
        # 读取要搜索的书名
        title = input("请输入书名（支持部分匹配）：").strip()
        # 先假设没找到，作为「是否命中」的标记
        found = False
        # 遍历书架查找同名图书
        for book in self.books:
            # 用 in 做模糊匹配：只要书名里包含输入的字就算命中
            if title in book.title:
                # 打印书籍信息（自动调用 __str__）
                print(book)
                # 命中就打上标记，避免后面误报「不存在」
                found = True
        # 遍历完毕，一本都没匹配上才提示
        if not found:
            print(f"图书：《{title}》不存在")
    # 列出全部：打印书架上的所有图书
    def list_books(self):
        # 先判断书架是否为空（空列表直接提示，不进循环）
        if not self.books:
            # 提示当前没有图书
            print("没有图书")
            # 结束方法
            return
        # 遍历书架
        for book in self.books:
            # 逐本打印（自动调用 __str__）
            print(book)
    # 从 books.json 读取图书数据到书架（重新加载会覆盖当前书架内容）
    def load_data(self):
        # 读取前先确认文件是否存在，不存在就直接返回，避免抛异常
        if not os.path.exists(DATA_FILE):
            # 提示没有数据文件
            print("数据文件不存在")
            # 结束方法
            return
        try:
            # 以只读、UTF-8 编码打开文件（with 语句保证用完后自动关闭）
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                # 把 JSON 文本解析成 Python 数据：这里是「字典组成的列表」
                data = json.load(f)
        # 文件内容不是合法 JSON，或文件读写出错（如被占用、无权限）
        except (json.JSONDecodeError, OSError) as e:
            # 打印失败原因，书架保持原样，不丢数据
            print(f"读取失败（{e}），书架保持原样")
            # 结束方法
            return
        # 先清空书架，保证重复加载时不会把旧数据叠加进来
        self.books = []
        # 遍历解析出来的每一个字典
        for book_dict in data:
            # 用字典里的四个字段创建 Book 对象（用关键字参数，顺序写错也不怕）
            book = Book(
                title=book_dict["title"],              # 书名
                author=book_dict["author"],            # 作者
                year=book_dict["year"],                # 年份
                price=book_dict["price"]               # 价格
            )
            # 把新建的 Book 对象放进书架
            self.books.append(book)
        # 循环结束后打印加载结果（注意与 for 平级，只打印一次）
        print(f"加载成功，共 {len(self.books)} 本书")
    # 把书架中的图书数据写入 books.json
    def save_data(self):
        # 准备空列表，用于存放待写入的字典
        data = []
        # 遍历书架
        for book in self.books:
            # 把每本 Book 对象转成字典后追加
            data.append({
                "title": book.title,                               # 书名
                "author": book.author,                             # 作者
                "year": book.year,                                 # 年份
                "price": book.price                                # 价格
            })
        # 以 UTF-8 写入方式打开文件（with 语句保证自动关闭）
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            # 写为 JSON：ensure_ascii=False 保留中文，indent=4 缩进美化
            json.dump(data, f, ensure_ascii=False, indent=4)
        # 打印保存成功提示
        print(f"已保存 {len(data)} 本图书")
    # 主循环：显示菜单并根据用户输入分发到各功能
    def run(self):
        # 无限循环，直到用户选择退出
        while True:
            # 打印空行 + 30 个等号作为分隔线
            print("\n" + "=" * 30)
            # 打印系统标题
            print("      个人图书管理系统")
            # 打印分隔线
            print("=" * 30)
            # 菜单项 1
            print("1. 添加图书")
            # 菜单项 2
            print("2. 删除图书")
            # 菜单项 3
            print("3. 修改价格")
            # 菜单项 4
            print("4. 搜索图书")
            # 菜单项 5
            print("5. 列出全部")
            # 菜单项 6
            print("6. 加载数据")
            # 菜单项 7
            print("7. 退出系统")
            # 打印分隔线
            print("=" * 30)
            # 捕获菜单输入的类型转换异常
            try:
                # 读取选项编号并转成整数
                choice = int(input("请输入选项编号："))
            # 输入内容无法转成整数
            except ValueError:
                # 提示输入无效
                print("输入无效，请输入数字！")
                # 跳过本次循环，重新显示菜单
                continue
            # 选项 1
            if choice == 1:
                # 调用添加图书
                self.add_book()
            # 选项 2
            elif choice == 2:
                # 调用删除图书
                self.del_book()
            # 选项 3
            elif choice == 3:
                # 调用修改价格
                self.update_book()
            # 选项 4
            elif choice == 4:
                # 调用搜索图书
                self.search_book()
            # 选项 5
            elif choice == 5:
                # 调用列出全部
                self.list_books()
            # 选项 6
            elif choice == 6:
                # 调用加载数据
                self.load_data()
            # 选项 7
            elif choice == 7:
                # 先保存数据
                self.save_data()
                # 跳出主循环，程序结束
                break
            # 其他数字
            else:
                # 提示选项不存在
                print("选项不存在，请重新输入！")

# 判断本文件是否作为脚本直接运行（而非被 import）
if __name__ == '__main__':
    # 创建 Library 实例
    library = Library()
    # 启动时自动加载历史数据
    library.load_data()
    # 启动主循环
    library.run()
