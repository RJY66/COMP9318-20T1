import collections as c


################# Question 1 #################
def dict_put_together(part1, part2):
    result = c.Counter(part1) + c.Counter(part2)
    return result


def pre_processing(training_data, data_set):
    for i in training_data:
        if i[1] in data_set:
            data_set[i[1]] = dict_put_together(part1=i[0], part2=data_set[i[1]])
        else:
            data_set[i[1]] = i[0]
    return data_set


def count_times(class_t, training_data):
    for i in training_data:
        if i[1] in class_t:
            class_t[i[1]] += 1
        else:
            class_t[i[1]] = 1
    return class_t


def count_total_times(class_t):
    sum = 0
    for v in class_t.values():
        sum += v
    return sum


def dataset_len_ham_or_spam(data_set, flag):
    if flag == 1:
        len_dataset_ham = 0
        for v1 in data_set['ham'].values():
            len_dataset_ham += v1
        return len_dataset_ham
    if flag == -1:
        len_dataset_spam = 0
        for v2 in data_set['spam'].values():
            len_dataset_spam += v2
        return len_dataset_spam


def set_put_together(part1, part2, new_set):
    for i in part1:
        new_set.add(i)
    for j in part2:
        new_set.add(j)
    return new_set


def multinomial_nb(training_data, sms):# do not change the heading of the function
    prob_class = 1
    data = dict()
    data = pre_processing(training_data=training_data, data_set=data)
    len_data_ham = dataset_len_ham_or_spam(data_set=data, flag=1)
    len_data_spam = dataset_len_ham_or_spam(data_set=data, flag=-1)
    word_set = set()
    word_set = set_put_together(part1=data['ham'], part2=data['spam'], new_set=word_set)
    class_t = {}
    class_t = count_times(class_t=class_t, training_data=training_data)
    total_times = count_total_times(class_t=class_t)
    percent_ham = class_t['ham'] / total_times
    percent_spam = class_t['spam'] / total_times
    percent_t = percent_spam / percent_ham
    for w in sms:
        freq_ham = 0
        freq_spam = 0
        if w in data['ham']:
            if w in data['spam']:
                freq_ham = data['ham'][w]
                freq_spam = data['spam'][w]
            else:
                freq_ham = data['ham'][w]
        else:
            if w in data['spam']:
                freq_spam = data['spam'][w]
            else:
                continue
        base_ham = len(word_set) + len_data_ham
        base_spam = len(word_set) + len_data_spam
        prob_ham = (1 + freq_ham) / base_ham
        prob_spam = (1 + freq_spam) / base_spam
        prob_class *= (prob_spam / prob_ham)
    prob_result = percent_t * prob_class
    return prob_result
