# -*- coding: utf-8 -*-
"""
Created By      : ZedFeorius
Created Time    : 2024/12/21 21:57
File Name       : user_model
Last Edit Time  : 
"""
from typing import List, Union, Dict, Any

from surf.modules.util import BaseModel
from surf.appsGlobal import logger


class UserModel(BaseModel):
    def __init__(self):
        super().__init__()

    def login(self, account: str, password: str, debug: bool = False) -> List[Union[Dict[str, str], None]]:
        """
        Login to the system
        :param account: user account id
        :param password: user's password
        :param debug: console log
        :return: a list of user id or None, if 'None' means user's
                 login failed(wrong password or account does not exist)
        """
        res = []
        try:
            query_sql = "SELECT c_user_id as id FROM public.t_users WHERE c_account_id = %s and c_password = %s;"
            user_id = self._pg.query(query_sql, [account, password])
            if debug:
                if not user_id:
                    logger.info("user login failed")
                else:
                    logger.info(f"account:{account}'s user_id：{user_id[0]}")
            res.extend(user_id)
        except Exception as e:
            logger.error(f"user: {account} login failed:{e}")
        finally:
            return res

    def get_user_data_by_id(self, user_id: str, debug: bool = False) -> List[Union[Dict[str, Any]]]:
        """
        get user data by user id
        :param user_id: user's uuid
        :param debug: console log
        :return: a lis of user's data or None, if 'None' means user not found
        """
        res = []
        try:
            query_sql = """
            SELECT 
                c_account_id as account,
                c_nickname as nickname,
                c_user_info as user_info
            FROM public.t_users WHERE c_user_id = %s
            """
            user_data = self._pg.query(query_sql, [user_id])
            if debug:
                if not user_data:
                    logger.info(f"invalid user_data:{user_data}")
                else:
                    logger.info(f"user:{user_id}'s user_data:{user_data}")
            res.extend(user_data)
        except Exception as e:
            logger.error(f"get user: {user_id}'s data failed:{e}")
        finally:
            return res

    def check_user_exist_by_email(self, email: str, debug: bool = False) -> bool:
        res = False
        try:
            query_sql = """
            SELECT count(1) FROM public.t_users WHERE c_user_info->>'email' = %s
            """
            res = True if self._pg.query(query_sql, [email])[0].get('count') == 1 else False
            if debug:
                if not res:
                    logger.info(f"invalid user_data:{email}")
                else:
                    logger.info(f"user:{email}'s user_data:{email}")
        except Exception as e:
            logger.error(f"check user exist by email:{email}:{e}")
        finally:
            return res


if __name__ == '__main__':
    um = UserModel()
    usr = um.login(account="otto", password="ottowantccb", debug=True)
    print(usr)
    data = um.get_user_data_by_id(user_id=usr[0]['id'])
    print(data)
