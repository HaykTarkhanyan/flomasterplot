# from urllib.request import urlopen
import io
import pandas as pd
# from colorthief import ColorThief

def get_data_type_for_given_feature(data_types, feature):
    for k in list(data_types.keys()):
        if feature in data_types[k]:
            if k == 'remove_cols' or k == 'binary':
                k = 'categorical'
            return k 
    return 'None'

def check_list_in_list(parent_list, sublist):
    for i in sublist:
        if i not in parent_list:
            return False
    return True

def add_labels_to_fig(fig, x, y, title):
    fig.update_layout(
        title=title,
        xaxis_title=x,
        yaxis_title=y
        )
        
def get_datetime_features(df, col):
    df['ds'] = pd.to_datetime(df[col])
    df['month'] = df.ds.dt.month
    import calendar
    df['month_english'] = df['month'].apply(lambda x: calendar.month_abbr[x])
    df['day_of_month'] = df.ds.dt.day
    df['year'] = df.ds.dt.year

    # https://pypi.org/project/holidays/
    # https://stackoverflow.com/questions/29688899/pandas-checking-if-a-date-is-a-holiday-and-assigning-boolean-value
    # cal = calendar()
    # holidays = cal.holidays(start=df.ds.min(), end=df.ds.max())

    # df['holiday'] = df['ds'].isin(holidays)
    
    df['day_of_week'] = df.ds.apply(lambda x: x.dayofweek)
    df['day_of_week_english'] = df['day_of_week'].map({0.0: 'Monday', 1.0: 'Tuesday', 2.0: 'Wednesday', \
                                                       3.0: 'Thursday', 4.0: 'Friday', 5.0:'Saturday', 6.0: "Sunday"})

    return df


# def get_color(logo_path_url, num_colors=2):  
#     if logo_path_url != '':
#         fd = urlopen(logo_path_url)
#         f = io.BytesIO(fd.read())
#         color_thief = ColorThief(f)
#         return color_thief.get_palette(color_count=num_colors)
#     else:
#         return ''

    