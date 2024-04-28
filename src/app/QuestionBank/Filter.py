

# 预留筛选器写法，从yelp直接粘贴过来未修改
# 后续数据库完善后再编写这部分


def filter_by_distance(filter_condition, df):
    filter_df = df
    if filter_condition == "1":
        filter_df = filter_df[filter_df["distance"] < 1000]

    elif filter_condition == "2":
        filter_df = filter_df[filter_df["distance"] < 2000]


    elif filter_condition == "5":
        filter_df = filter_df[filter_df["distance"] < 5000]

    return filter_df


def filter_by_stars(filter_condition,df):
    if filter_condition == "5":
        filter_df = df[df["stars"] == 5]

    elif filter_condition == "4":
        filter_df = df[df["stars"] >= 4]

    elif filter_condition == "3":
        filter_df = df[df["stars"] >= 3]

    return filter_df

def filter(df,filter_conditions):

    result_df = df

    #遍历筛选条件
    for filter_type, filter_condition in filter_conditions.items():
        if filter_type == "distance":
            result_df = filter_by_distance(filter_condition, result_df)
        elif filter_type == "stars":
            result_df = filter_by_stars(filter_condition, result_df)
        elif filter_type == "facilities":
            pass
        else:
            pass  # 预留其他条件

    return result_df


# 实现排序函数
def sort(df,sortBy):
    if sortBy == 'stars':
        df = df.sort_values(by='stars', ascending=False)
        return df
    elif sortBy == 'review_count':
        df = df.sort_values(by='review_count', ascending=False)
        return df
    elif sortBy == 'distance':
        df = df.sort_values(by='distance')
        return df
    else:
        return df
