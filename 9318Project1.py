import numpy as np
import pickle
import time


def pq(data, P, init_centroids, max_iter):
    def Split_P_data(Data_File, p):
        data = np.array(Data_File)
        data = np.array_split(data, p, axis=1)
        return data

    def Update_centr(p, centroids, data, N_cluster):
        for i_p in range(p):
            for j_index, j_row in enumerate(data[i_p]):
                # one of data to all centers distance
                one_L1_dis = np.sum(abs(centroids[i_p] - j_row), axis=1)
                one_L1 = np.where(one_L1_dis == np.min(one_L1_dis, axis=0))
                N_cluster[i_p][j_index] = one_L1[0][0]
        for i_p in range(p):
            for j_index, j_row in enumerate(centroids[i_p]):
                indexs = np.where(N_cluster[i_p] == j_index)
                if len(indexs[0]) == 0:
                    continue
                else:
                    for d_index, d in enumerate(indexs[0]):
                        if d_index == 0:
                            line = np.array([data[i_p][d]])
                        else:
                            line = np.vstack((line, data[i_p][d]))
                    # update onelne of centroid
                    centroids[i_p][j_index] = np.median(line, axis=0)
        return centroids, N_cluster

    def K_means(p, centroids, data, N_cluster, max_iter):
        for i in range(max_iter):
            centroids, N_cluster = Update_centr(p, centroids, data, N_cluster)
        # final half update N_cluster
        for i_p in range(p):
            for j_index, j_row in enumerate(data[i_p]):
                # one of data to all centers distance
                one_L1_dis = np.sum(abs(centroids[i_p] - j_row), axis=1, dtype='float32')
                # find the min one for this row
                one_L1 = np.where(one_L1_dis == np.min(one_L1_dis, axis=0))
                N_cluster[i_p][j_index] = one_L1[0][0]
        return centroids, N_cluster
    data = Split_P_data(data, P)
    centroids = np.array(init_centroids, dtype='float32')
    # we can get p*N*1 array
    N_cluster = np.zeros([len(data[0]), P], dtype='uint8')
    N_cluster = np.array_split(N_cluster, P, axis=1)
    # assign value of N_cluster
    centroids, N_cluster = K_means(P, centroids, data, N_cluster, max_iter)
    a = N_cluster[0]
    for i in range(len(N_cluster)):
        if i == 0:
            continue
        a = np.hstack((a, N_cluster[i]))
    N_cluster = a
    # codebooks code
    return centroids, N_cluster


def query(queries, codebooks, codes, T):
    def caculate_one_p_line_dis(queries, codebooks, p):
        queries = np.array_split(queries, p, axis=0)
        a = np.zeros([256, p])
        for i in range(p):
            a[:, i] = np.sum(abs(codebooks[i] - queries[i]), axis=1)
        return a

    p = len(codes[0])
    QKP_dis_table = np.zeros([len(queries), 256, p])
    test = np.zeros([len(queries), 256, p])
    h = 0
    for i in range(len(queries)):
        one_line_queries = queries[i].T
        QKP_dis_table[i] = caculate_one_p_line_dis(one_line_queries, codebooks, p)

    dis_query_n = np.zeros([len(codes), 1])
    q_dis_query_n = np.zeros([len(queries), len(codes), 1])

    for q_index in range(len(queries)):
        for i in range(len(codes)):
            one_line_codes = []
            p_index = 0
            for j in codes[i]:
                one_line_codes.append(QKP_dis_table[q_index][j][p_index])
                p_index += 1
            dis_query_n[i] = sum(one_line_codes)
        q_dis_query_n[q_index] = dis_query_n
    sort_q_n = np.zeros([len(queries), len(codes), 1])
    for i in range(len(queries)):
        sort_q_dis_query_n = np.argsort(q_dis_query_n[i].T)
        sort_q_n[i] = sort_q_dis_query_n.T
    answer = set()
    answers = []
    for q_index in range(len(queries)):
        answer = set()
        t = 1
        extra = T
        for i in range(T):
            answer.add(int(sort_q_n[q_index][i][0]))
        last_one = sort_q_n[q_index][i][0]

        while t:

            next_one = sort_q_n[q_index][extra][0]
            if q_dis_query_n[q_index][int(next_one)][0] == q_dis_query_n[q_index][int(last_one)][0]:
                answer.add(int(next_one))
                extra += 1
            else:
                t = 0

        answers.append(answer)
    return answers


# How to run your implementation for Part 1
with open('./toy_example/Data_File', 'rb') as f:
    data = pickle.load(f, encoding='bytes')
with open('./toy_example/Centroids_File', 'rb') as f:
    centroids = pickle.load(f, encoding='bytes')
start = time.time()
codebooks, codes = pq(data, P=2, init_centroids=centroids, max_iter=20)
end = time.time()
time_cost_1 = end - start
print(f"Part1: {time_cost_1} s")

# How to run your implementation for Part 2
with open('./toy_example/Query_File', 'rb') as f:
    queries = pickle.load(f, encoding='bytes')
start = time.time()
candidates = query(queries, codebooks, codes, T=10)
end = time.time()
time_cost_2 = end - start
print(f"Part2: {time_cost_2} s")
print(candidates)
