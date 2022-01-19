def get_data_type_for_given_feature(data_types, feature):
    for k in list(data_types.keys()):
        if feature in data_types[k]:
            if k == 'remove_cols' or k == 'binary':
                k = 'categorical'
            return k 
    return 'None'