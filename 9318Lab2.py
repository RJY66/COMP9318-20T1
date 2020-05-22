## import modules here
import pandas as pd
import numpy as np
import helper

################### Question 1 ###################


def single_line_opt(row, col):
    dims = row[:-1][1-col:]
    dim = len(dims)
    result = []
    for i in range(0, 2 ** dim):
        new_row = list(row)
        for j in range(0, dim):
            gap = 2 ** j
            if i % (2 * gap) > gap - 1:
                new_row[len(new_row) - j - 2] = 'ALL'
        result.append(new_row)
    return result


def buc_rec_3_params(input, result, pre=[]):
    rows = input.shape[0]
    dims = input.shape[1]
    new_pre = pre.copy()
    if dims >= 2 and rows == 1:
        new_pre += input.iloc[0, ].tolist()
        new_rows = single_line_opt(tuple(new_pre), dims)
        result += new_rows
        return result
    elif dims == 1:
        # only the measure dim
        input_sum = sum(helper.project_data(input, 0))
        new_pre.append(input_sum)
        result.append(new_pre)
        return result
    else:
        # the general case
        dim0_vals = set(helper.project_data(input, 0).values)
        for dim0_v in dim0_vals:
            new_pre.append(dim0_v)
            sub_data = helper.slice_data_dim0(input, dim0_v)
            result = buc_rec_3_params(sub_data, result, new_pre)
            new_pre = pre.copy()
        ## for R_{ALL}
        sub_data = helper.remove_first_dim(input)
        new_pre.append('ALL')
        result = buc_rec_3_params(sub_data, result, new_pre)
        return result


def buc_rec_optimized(df):# do not change the heading of the function
    result = []
    result = buc_rec_3_params(input=df, result=result)
    result = pd.DataFrame(result, columns=df.columns.values)
    return result
