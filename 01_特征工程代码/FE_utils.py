#在创建新特征时，程序需要调用此处的程序，程序从上一部生成的dataframe格式中，通过关键字得到所需要的值
def find_user_hour_C14(x,y,z,group_dict):
    value=group_dict.loc[(group_dict['user_id']==x)&(group_dict['hour']==y)&(group_dict['C14']==z),0]
    value=int(value)
    return value

def find_user_hour_C17(x,y,z,group_dict):
    value=group_dict.loc[(group_dict['user_id']==x)&(group_dict['hour']==y)&(group_dict['C17']==z),0]
    value=int(value)
    return value

def find_user_day_C14(x,y,z,group_dict):
    value=group_dict.loc[(group_dict['user_id']==x)&(group_dict['hour_days']==y)&(group_dict['C14']==z),0]
    value=int(value)
    return value

def find_user_day_C17(x,y,z,group_dict):
    value=group_dict.loc[(group_dict['user_id']==x)&(group_dict['hour_days']==y)&(group_dict['C17']==z),0]
    value=int(value)
    return value

def find_user_day_times(x,y,group_dict):
    value=group_dict.loc[(group_dict['user_id']==x)&(group_dict['hour_days']==y),0]
    value=int(value)
    return value

def find_user_day_app_id(x,y,z,group_dict):
    value=group_dict.loc[(group_dict['user_id']==x)&(group_dict['hour_days']==y)&(group_dict['app_id']==z),0]
    value=int(value)
    return value

def find_user_days(x,group_dict):
    value=group_dict.loc[(group_dict['user_id']==x),0]
    value=int(value)
    return value