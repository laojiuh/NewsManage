import time
from colorama import Fore, Style
from getpass import getpass
from service.role_service import RoleServer
from service.user_service import UserService
from service.news_service import NewsService
from service.type_service import TypeService
import os
import sys

__user_service = UserService()
__news_service = NewsService()
__role_service = RoleServer()
__type_service = TypeService()

while True:
    os.system('cls')
    print(Fore.LIGHTBLUE_EX, "\n{}".format('=' * 120))
    print(Fore.LIGHTBLUE_EX, "\n{}欢迎使用新闻管理系统".format(' ' * 50))
    print(Fore.LIGHTBLUE_EX, "\n{}".format('=' * 120))
    print(Fore.LIGHTYELLOW_EX, "\n{}1.登录系统".format(' ' * 50))
    print(Fore.LIGHTYELLOW_EX, "\n{}2.退出系统".format(' ' * 50))
    print(Style.RESET_ALL)
    opt = input('\n{}输入操作编号:'.format(' ' * 50))

    if opt == '1':
        username = input('\n{}用户名:'.format(' ' * 50))
        # print(username)
        password = getpass('\n{}密码:'.format(' ' * 50))
        # print(password)
        result = __user_service.login(username, password)
        # 登录成功
        if result:
            # 查询角色身份
            role = __user_service.search_user_role(username)
            while True:
                os.system('cls')
                if role == '新闻编辑':
                    print(Fore.LIGHTGREEN_EX, "\n{}1.发表新闻".format(' ' * 50))
                    print(Fore.LIGHTGREEN_EX, "\n{}2.编辑新闻".format(' ' * 50))
                    print(Fore.LIGHTRED_EX, "\n{}back.退出登录".format(' ' * 50))
                    print(Fore.LIGHTRED_EX, "\n{}exit.退出系统".format(' ' * 50))
                    print(Style.RESET_ALL)
                    opt = input('\n{}输入操作编号:'.format(' ' * 50))
                    # 发表新闻操作
                    if opt == '1':
                        os.system('cls')
                        print(Fore.LIGHTGREEN_EX, "\n{}请输入新闻相关信息".format(' ' * 50))
                        print(Style.RESET_ALL)
                        title = input("\n{}新闻标题:".format(' ' * 50))
                        userid = __user_service.search_userid(username)
                        result = __type_service.search_list()
                        # 显示可选择的新闻类型
                        for index in range(len(result)):
                            one = result[index]
                            print(Fore.LIGHTBLUE_EX, "\n{0}{1}{2}".format(' ' * 50, index + 1, one[1]))
                        print(Style.RESET_ALL)
                        opt = input("\n{}新闻类型编号:".format(' ' * 50))
                        type_id = result[int(opt) - 1][0]
                        # TODO 新闻正文内容
                        path = input("\n{}输入文件路径:".format(' ' * 50))
                        file = open(path, 'rb')
                        content = file.read().decode('utf-8')
                        file.close()
                        is_top = input("\n{}置顶级别(0-5):".format(' ' * 50))
                        is_commite = input("\n{}是否提交(Y/N):".format(' ' * 50))
                        if is_commite == 'Y' or 'y':
                            __news_service.insert(title, userid, type_id, content, is_top)
                            print("\n{}保存成功(3秒自动返回)".format(' ' * 50))
                            time.sleep(3)

                    # 编辑新闻
                    elif opt == '2':
                        page = 1
                        while True:
                            os.system('cls')
                            count_page = __news_service.search_count_page()
                            show_news = __news_service.search_list(page)
                            for index in range(len(show_news)):
                                one = show_news[index]
                                print(Fore.LIGHTBLUE_EX,
                                      "\n{0}{1}\t{2}\t{3}\t{4}".format(' ' * 40, index + 1, one[1], one[2],
                                                                       one[3]))
                            print(Fore.LIGHTRED_EX, "\n{}".format('-' * 120))
                            print(Fore.LIGHTBLUE_EX, '{0}{1}/{2}'.format(' ' * 50, page, count_page))
                            print(Fore.LIGHTRED_EX, "\n{}".format('-' * 120))
                            print(Fore.LIGHTRED_EX, "\n{}back.返回上一层".format(' ' * 50))
                            print(Fore.LIGHTRED_EX, "\n{}prev.上一页".format(' ' * 50))
                            print(Fore.LIGHTRED_EX, "\n{}next.下一页".format(' ' * 50))
                            print(Style.RESET_ALL)
                            opt = input('\n{}输入操作编号:'.format(' ' * 50))
                            if opt == 'back':
                                break
                            elif opt == 'prev':
                                if page > 1:
                                    page -= 1
                            elif opt == 'next':
                                if page < count_page:
                                    page += 1
                            elif opt.isdigit():
                                if 1 <= int(opt) <= 10 and int(opt) <= len(show_news):
                                    os.system('cls')
                                    # 修改新闻的内容
                                    news_id = show_news[int(opt) - 1][0]
                                    print("\n{0}新闻id号:{1}".format(' ' * 50, news_id))
                                    result = __news_service.search_by_id(news_id)
                                    title = result[0]
                                    type = result[1]
                                    is_top = result[2]
                                    print("\n{0}新闻原标题:{1}".format(' ' * 50, title))
                                    new_title = input('\n{}新标题:'.format(' ' * 50))
                                    print("\n{0}新闻原类型: {1}".format(' ' * 50, type))
                                    result = __type_service.search_list()
                                    # 显示可选择的新闻类型
                                    for index in range(len(result)):
                                        one = result[index]
                                        print(Fore.LIGHTBLUE_EX, "\n{0}{1}{2}".format(' ' * 50, index + 1, one[1]))
                                    print(Style.RESET_ALL)
                                    opt = input("\n{}类型编号:".format(' ' * 50))
                                    type_id = result[int(opt) - 1][0]
                                    # TODO 新闻内容
                                    path = input("\n{}输入文件路径:".format(' ' * 50))
                                    file = open(path, 'rb')
                                    content = file.read().decode('utf-8')
                                    file.close()
                                    print("\n{0}新闻原置顶级别:{1}".format(' ' * 50, is_top))
                                    new_is_top = input('\n{}置顶级别(0-5):'.format(' ' * 50))
                                    is_commite = input('\n{}是否提交(Y/N):'.format(' ' * 50))
                                    if is_commite == 'Y' or 'y':
                                        __news_service.update(news_id, new_title, type_id, content, new_is_top)
                                        print("\n{}保存成功(3秒自动返回)".format(' ' * 50))
                                        time.sleep(3)

                    elif opt == 'back':
                        break
                    elif opt == 'exit':
                        sys.exit(0)

                elif role == '管理员':
                    print(Fore.LIGHTGREEN_EX, "\n{}1.新闻管理".format(' ' * 50))
                    print(Fore.LIGHTGREEN_EX, "\n{}2.用户管理".format(' ' * 50))
                    print(Fore.LIGHTRED_EX, "\n{}back.退出登录".format(' ' * 50))
                    print(Fore.LIGHTRED_EX, "\n{}exit.退出系统".format(' ' * 50))
                    print(Style.RESET_ALL)
                    opt = input('\n{}输入操作编号:'.format(' ' * 50))

                    # 进行新闻管理操作
                    if opt == '1':
                        while True:
                            os.system('cls')
                            print(Fore.LIGHTGREEN_EX, "\n{}1.审批新闻".format(' ' * 50))
                            print(Fore.LIGHTGREEN_EX, "\n{}2.删除新闻".format(' ' * 50))
                            print(Fore.LIGHTRED_EX, "\n{}back.返回上一层".format(' ' * 50))
                            print(Style.RESET_ALL)
                            opt = input('\n{}输入操作编号:'.format(' ' * 50))
                            # 审批新闻
                            if opt == '1':
                                page = 1
                                while True:
                                    os.system('cls')
                                    count_page = __news_service.search_unreview_count_page()
                                    show_news = __news_service.search_unreview_list(page)
                                    for index in range(len(show_news)):
                                        one = show_news[index]
                                        print(Fore.LIGHTBLUE_EX,
                                              "\n{0}{1}\t{2}\t{3}\t{4}".format(' ' * 40, index + 1, one[1], one[2],
                                                                               one[3]))
                                    print(Fore.LIGHTRED_EX, "\n{}".format('-' * 120))
                                    print(Fore.LIGHTBLUE_EX, '{0}{1}/{2}'.format(' ' * 50, page, count_page))
                                    print(Fore.LIGHTRED_EX, "\n{}".format('-' * 120))
                                    print(Fore.LIGHTRED_EX, "\n{}back.返回上一层".format(' ' * 50))
                                    print(Fore.LIGHTRED_EX, "\n{}prev.上一页".format(' ' * 50))
                                    print(Fore.LIGHTRED_EX, "\n{}next.下一页".format(' ' * 50))
                                    print(Style.RESET_ALL)
                                    opt = input('\n{}输入操作编号:'.format(' ' * 50))
                                    if opt == 'back':
                                        break
                                    elif opt == 'prev':
                                        if page > 1:
                                            page -= 1
                                    elif opt == 'next':
                                        if page < count_page:
                                            page += 1
                                    elif opt.isdigit():
                                        if 1 <= int(opt) <= 10 and int(opt) <= len(show_news):
                                            news_id = show_news[int(opt) - 1][0]
                                            __news_service.update_unreview_news(news_id)
                                            result = __news_service.search_cache(news_id)
                                            title = result[0]
                                            username = result[1]
                                            type = result[2]
                                            content_id = result[3]
                                            # TODO 查找新闻正文在mogodb中
                                            content = __news_service.search_content_by_id(content_id)
                                            is_top = result[4]
                                            create_time = str(result[5])
                                            __news_service.cache_news(news_id, title, username, type, content, is_top,
                                                                      create_time)

                            # 删除新闻
                            elif opt == '2':
                                page = 1
                                while True:
                                    os.system('cls')
                                    count_page = __news_service.search_count_page()
                                    show_news = __news_service.search_list(page)
                                    for index in range(len(show_news)):
                                        one = show_news[index]
                                        print(Fore.LIGHTBLUE_EX,
                                              "\n{0}{1}\t{2}\t{3}\t{4}".format(' ' * 40, index + 1, one[1], one[2],
                                                                               one[3]))
                                    print(Fore.LIGHTRED_EX, "\n{}".format('-' * 120))
                                    print(Fore.LIGHTBLUE_EX, '{0}{1}/{2}'.format(' ' * 50, page, count_page))
                                    print(Fore.LIGHTRED_EX, "\n{}".format('-' * 120))
                                    print(Fore.LIGHTRED_EX, "\n{}back.返回上一层".format(' ' * 50))
                                    print(Fore.LIGHTRED_EX, "\n{}prev.上一页".format(' ' * 50))
                                    print(Fore.LIGHTRED_EX, "\n{}next.下一页".format(' ' * 50))
                                    print(Style.RESET_ALL)
                                    opt = input('\n{}输入操作编号:'.format(' ' * 50))
                                    if opt == 'back':
                                        break
                                    elif opt == 'prev':
                                        if page > 1:
                                            page -= 1
                                    elif opt == 'next':
                                        if page < count_page:
                                            page += 1
                                    elif opt.isdigit():
                                        if 1 <= int(opt) <= 10 and int(opt) <= len(show_news):
                                            news_id = show_news[int(opt) - 1][0]
                                            __news_service.delete_by_id(news_id)
                                            __news_service.delete_cache(news_id)

                            elif opt == 'back':
                                break
                    # 进行用户管理操作
                    elif opt == '2':
                        while True:
                            os.system('cls')
                            print(Fore.LIGHTGREEN_EX, "\n{}1.添加用户".format(' ' * 50))
                            print(Fore.LIGHTGREEN_EX, "\n{}2.修改用户".format(' ' * 50))
                            print(Fore.LIGHTGREEN_EX, "\n{}3.删除用户".format(' ' * 50))
                            print(Fore.LIGHTRED_EX, "\n{}back.返回上一层".format(' ' * 50))
                            print(Style.RESET_ALL)
                            opt = input('\n{}输入操作编号:'.format(' ' * 50))
                            if opt == '1':
                                os.system('cls')
                                username = input("\n{}用户名:".format(' ' * 50))
                                password = getpass("\n{}密码:".format(' ' * 50))
                                repassword = getpass("\n{}再次输入密码:".format(' ' * 50))
                                if password != repassword:
                                    print("\n{}两次密码不一致(3秒自动返回)".format(' ' * 50))
                                    time.sleep(3)
                                    continue
                                email = input("\n{}邮箱:".format(' ' * 50))
                                result = __role_service.search_list()
                                # 显示可选择的用户身份
                                for index in range(len(result)):
                                    one = result[index]
                                    print(Fore.LIGHTBLUE_EX, "\n{0}{1}{2}".format(' ' * 50, index + 1, one[1]))
                                print(Style.RESET_ALL)
                                opt = input("\n{}角色编号:".format(' ' * 50))
                                role_id = result[int(opt) - 1][0]
                                __user_service.insert(username, password, email, role_id)
                                print("\n{}保存成功(3秒自动返回)".format(' ' * 50))
                                time.sleep(3)
                            elif opt == '2':
                                page = 1
                                while True:
                                    os.system('cls')
                                    count_page = __user_service.search_count_page()
                                    show_news = __user_service.search_list(page)
                                    for index in range(len(show_news)):
                                        one = show_news[index]
                                        print(Fore.LIGHTBLUE_EX,
                                              "\n{0}{1}\t{2}\t{3}".format(' ' * 40, index + 1, one[1], one[2]))
                                    print(Fore.LIGHTRED_EX, "\n{}".format('-' * 120))
                                    print(Fore.LIGHTBLUE_EX, '{0}{1}/{2}'.format(' ' * 50, page, count_page))
                                    print(Fore.LIGHTRED_EX, "\n{}".format('-' * 120))
                                    print(Fore.LIGHTRED_EX, "\n{}back.返回上一层".format(' ' * 50))
                                    print(Fore.LIGHTRED_EX, "\n{}prev.上一页".format(' ' * 50))
                                    print(Fore.LIGHTRED_EX, "\n{}next.下一页".format(' ' * 50))
                                    print(Style.RESET_ALL)
                                    opt = input('\n{}输入操作编号:'.format(' ' * 50))
                                    if opt == 'back':
                                        break
                                    elif opt == 'prev':
                                        if page > 1:
                                            page -= 1
                                    elif opt == 'next':
                                        if page < count_page:
                                            page += 1
                                    elif opt.isdigit():
                                        if 1 <= int(opt) <= 10 and int(opt) <= len(show_news):
                                            os.system('cls')
                                            user_id = show_news[int(opt) - 1][0]
                                            print('\n{}请输入修改用户的新信息:'.format(' ' * 50))
                                            username = input('\n{}新用户名:'.format(' ' * 50))
                                            password = getpass("\n{}新密码:".format(' ' * 50))
                                            repassword = getpass("\n{}再次输入密码:".format(' ' * 50))
                                            if password != repassword:
                                                print(Fore.LIGHTRED_EX, "\n{}两次密码不一致(3秒自动返回)".format(' ' * 50))
                                                print(Style.RESET_ALL)
                                                time.sleep(3)
                                                break
                                            email = input("\n{}新邮箱:".format(' ' * 50))
                                            result = __role_service.search_list()
                                            # 显示可选择的用户身份
                                            for index in range(len(result)):
                                                one = result[index]
                                                print(Fore.LIGHTBLUE_EX,
                                                      "\n{0}{1}{2}".format(' ' * 50, index + 1, one[1]))
                                            print(Style.RESET_ALL)
                                            opt = input("\n{}角色编号:".format(' ' * 50))
                                            role_id = result[int(opt) - 1][0]
                                            opt = input("\n{}是否保存(Y/N):".format(' ' * 50))
                                            if opt == 'Y' or 'y':
                                                __user_service.update(user_id, username, password, email, role_id)
                                                print("\n{}保存成功(3秒自动返回)".format(' ' * 50))
                                                time.sleep(3)
                            elif opt == '3':
                                page = 1
                                while True:
                                    os.system('cls')
                                    count_page = __user_service.search_count_page()
                                    show_news = __user_service.search_list(page)
                                    for index in range(len(show_news)):
                                        one = show_news[index]
                                        print(Fore.LIGHTBLUE_EX,
                                              "\n{0}{1}\t{2}\t{3}".format(' ' * 40, index + 1, one[1], one[2]))
                                    print(Fore.LIGHTRED_EX, "\n{}".format('-' * 120))
                                    print(Fore.LIGHTBLUE_EX, '{0}{1}/{2}'.format(' ' * 50, page, count_page))
                                    print(Fore.LIGHTRED_EX, "\n{}".format('-' * 120))
                                    print(Fore.LIGHTRED_EX, "\n{}back.返回上一层".format(' ' * 50))
                                    print(Fore.LIGHTRED_EX, "\n{}prev.上一页".format(' ' * 50))
                                    print(Fore.LIGHTRED_EX, "\n{}next.下一页".format(' ' * 50))
                                    print(Style.RESET_ALL)
                                    opt = input('\n{}输入操作编号:'.format(' ' * 50))
                                    if opt == 'back':
                                        break
                                    elif opt == 'prev':
                                        if page > 1:
                                            page -= 1
                                    elif opt == 'next':
                                        if page < count_page:
                                            page += 1
                                    elif opt.isdigit():
                                        if 1 <= int(opt) <= 10 and int(opt) <= len(show_news):
                                            os.system('cls')
                                            user_id = show_news[int(opt) - 1][0]
                                            __user_service.delete_by_id(user_id)
                                            print("\n{}删除成功(3秒自动返回)".format(' ' * 50))
                                            time.sleep(3)

                            elif opt == 'back':
                                break

                    elif opt == 'back':
                        break
                    elif opt == 'exit':
                        sys.exit(0)
                else:
                    print('失败')
                    sys.exit(0)
        # 登录失败
        else:
            print('\n{}登录失败(3秒自动返回)'.format(' ' * 50))
            time.sleep(3)
    elif opt == "2":
        sys.exit(0)
