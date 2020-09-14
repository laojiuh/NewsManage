from db.mysql_db import pool



class TypeDao:
    # 查询新闻类型
    def search_list(self):
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = 'SELECT id,type FROM t_type ORDER BY id  '
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(e)
        finally:
            if 'con' in dir():
                con.close()


# if __name__ == '__main__':
#     kk = TypeDao()
#     res=kk.search_list()
#     print(res)
