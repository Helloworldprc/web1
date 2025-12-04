"""
________________________________________
发件人: potato <15238515292@163.com>
发送时间: 2025年12月3日 21:35
收件人: facethatdifficult@Outlook.com <facethatdifficult@Outlook.com>
主题: SQLITE_FAST"""
 
from sqlite3 import connect, Error

def new_file(new_file_name: str) -> None:
    """
    创建或连接数据库文件，全局初始化 conn 和 cursor
    :param new_file_name: 数据库文件名（无需 .db 后缀）
    :raises: 如果连接失败，抛出 RuntimeError
    """
    global conn, cursor
    try:
        conn = connect(new_file_name + '.db')
        cursor = conn.cursor()
    except Error as e:
        raise RuntimeError(f"数据库连接失败: {e}")

class Table:
    def __init__(self, table_name: str, **project: str):
        """
        创建表
        :param table_name: 表名
        :param project: 列名及数据类型（如 name="TEXT(20)"）
        :raises: 如果表创建失败，抛出 RuntimeError
        """
        self.table_name = table_name
        self.columns = list(project.keys())
        try:
            # 拼接列定义（例如：id INTEGER, name TEXT）
            columns_def = ", ".join([f"{k} {v}" for k, v in project.items()])
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})")
        except Error as e:
            raise RuntimeError(f"创建表 {table_name} 失败: {e}")

    def write(self, *items: str) -> bool:
        """
        插入数据
        :param items: 按列顺序传入数据
        :return: 成功返回 True，失败返回 False
        """
        try:
            placeholders = ", ".join(["?"] * len(items))
            sql = f"INSERT INTO {self.table_name} VALUES ({placeholders})"
            cursor.execute(sql, items)
            conn.commit()
            return True
        except Error as e:
            print(f"插入数据失败: {e}")
            conn.rollback()  # 回滚事务
            return False

    def read_all(self) -> list:
        """读取所有数据，失败返回空列表"""
        try:
            cursor.execute(f"SELECT * FROM {self.table_name}")
            return cursor.fetchall()
        except Error as e:
            print(f"读取数据失败: {e}")
            return []

    def search(self, search):
        """
        检索
        :param search: 依据
        :return: 检索结果
        """
        try:
            cursor.execute(
            f"SELECT * FROM {self.table_name} WHERE " + search

            )
            return cursor.fetchall()
        except:
            return 'not found'

    def delete(self, delete):
        """
        删除
        :param delete: 删除项目
        :return: None
        """
        try:
            cursor.execute('delete from ' + self.table_name + 'where ' + delete)
        except:
            return "失败"

    def update(self, search, set):
        """
        更改
        :param search: 你要找的项目
        :param set: 更改依据
        :return: None
        """
        cursor.execute('update ' + self.table_name + ' set ' + set + " where " + search)

def close() -> None:
    """安全关闭连接"""
    try:
        cursor.close()
        conn.commit()
        conn.close()
    except Error as e:
        print(f"关闭连接时出错: {e}")

