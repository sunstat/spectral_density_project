import os
from spectral_density import *
from generate_weights import *
import pickle
import random
import matplotlib.pyplot as plt
from datetime import datetime
import sys
RES_DIR = 'result'
simu_log_file = 'simu_res.log'


p_values = [12,48,96]



def fetch_span(num_obs):
    if num_obs == 800:
        return 30
    elif num_obs == 600:
        return 24
    elif num_obs == 400:
        return 20


def extract_tuple1(errs_dict):
    ls = sorted(errs_dict.items())
    freq_ind, values = zip(*ls)
    return freq_ind, values



def test_left_right_norm(spec_est):
    res_sm = {}
    res_sh = {}
    res_th = {}
    for n in range(-399, 400, 1):
        res_sm[n] = HS_norm(spec_est.query_smoothing_estimator(n))
        res_sh[n] = HS_norm(spec_est.query_shrinkage_estimator(n))
        res_th[n] = HS_norm(spec_est.query_thresholding_estimator(n))
    #keys, values = extract_tuple1(res_sm)
    #pyplot.plot(keys, values, 'ro', label='smoothed')
    keys, values = extract_tuple1(res_th)
    plt.plot(keys, values, 'y2', label='thresholding')
    keys, values = extract_tuple1(res_sh)
    plt.plot(keys, values, 'g+', label='shrinkage')
    plt.show()




def append_help(ls1, ls2, ls3, v1, v2, v3):
    ls1.append(v1)
    ls2.append(v2)
    ls3.append(v3)



def mean_values(dict_values, true_spectral):
    return np.mean(list(dict_values.values()))/np.mean(list(true_spectral.values()))


def append_relative_err(result):

    errs_dict_sm = result['raw_error']['sm']
    errs_dict_sh = result['raw_error']['sh']
    errs_dict_th = result['raw_error']['th']
    errs_dict_so = result['raw_error']['so']
    errs_dict_al = result['raw_error']['al']
    true_spectral = result['raw_error']['true']

    errs_dict_sm = list(map(lambda x: mean_values(x, true_spectral), errs_dict_sm))
    errs_dict_sh = list(map(lambda x: mean_values(x, true_spectral), errs_dict_sh))
    errs_dict_th = list(map(lambda x: mean_values(x, true_spectral), errs_dict_th))
    errs_dict_al = list(map(lambda x: mean_values(x, true_spectral), errs_dict_al))
    errs_dict_so = list(map(lambda x: mean_values(x, true_spectral), errs_dict_so))

    err_al = np.mean(errs_dict_al)
    err_th = np.mean(errs_dict_th)
    err_so = np.mean(errs_dict_so)
    err_sh = np.mean(errs_dict_sh)
    err_sm = np.mean(errs_dict_sm)

    std_sm = np.std(errs_dict_sm)
    std_sh = np.std(errs_dict_sh)
    std_th = np.std(errs_dict_th)
    std_al = np.std(errs_dict_al)
    std_so = np.std(errs_dict_so)


    result['relative_error'] = {}
    for method in ['al', 'th', 'so', 'sh', 'sm']:
        result['relative_error'][method] = (eval('err_'+method), eval('std_'+method))

    return result




def simu_help(mode, num_obs, p, generating_mode):
    assert generating_mode in ['ma', 'var']
    print("now doing simulation with setting p = {}, mode = {}".format(p, mode))
    print("================")
    weights = fetch_weights(p, mode, generating_mode)
    stdev = 1
    span = fetch_span(num_obs)

    model_info = {}
    model_info['model'] = generating_mode
    model_info['weights'] = weights
    model_info['span'] = span
    model_info['stdev'] = stdev


    errs_dict_al = []
    errs_dict_th = []
    errs_dict_so = []
    errs_dict_sh = []
    errs_dict_sm = []

    precision_al = []
    precision_th= []
    precision_so = []
    recall_al = []
    recall_so = []
    recall_th = []
    F1_al = []
    F1_so = []
    F1_th = []

    true_spectral_norm_square = {}


    for i in range(5):
        if generating_mode == 'ma':
            ts = generate_ma(weights, num_obs=num_obs, stdev=stdev)
        elif generating_mode == 'var':
            ts = generate_mvar(weights, num_obs=num_obs, stdev=stdev)
        spec_est = SpecEst(ts, model_info)
        #test_left_right_norm(spec_est)
        err_al_dict = spec_est.evaluate('al')
        err_th_dict = spec_est.evaluate('th')
        err_so_dict = spec_est.evaluate('so')
        err_sh_dict = spec_est.evaluate('sh')
        err_sm_dict = spec_est.evaluate('sm')

        errs_dict_al.append(err_al_dict)
        errs_dict_th.append(err_th_dict)
        errs_dict_so.append(err_so_dict)
        errs_dict_sh.append(err_sh_dict)
        errs_dict_sm.append(err_sm_dict)
        for mode in ['th', 'so', 'al']:
            precision, recall, F1 = spec_est.query_recover_three_measures(mode)
            if mode == 'th':
                append_help(precision_th, recall_th, F1_th, precision, recall, F1)
            elif mode == 'so':
                append_help(precision_so, recall_so, F1_so, precision, recall, F1)
            elif mode == 'al':
                append_help(precision_al, recall_al, F1_al, precision, recall, F1)

        if i == 0:
            true_spectral = spec_est.return_all_true_spectral()
            for key in true_spectral:
                true_spectral_norm_square[key] = HS_norm(true_spectral[key])**2
        print("finishing iteration {}".format(i))

    result = {}

    result['raw_error'] = {'al': errs_dict_al, 'th': errs_dict_th, 'so':errs_dict_so,
                       'sh': errs_dict_sh, 'sm': errs_dict_sm, 'true': true_spectral_norm_square}
    result['precision'] = {'so': (np.mean(precision_so), np.std(precision_so)), 'al': (np.mean(precision_al), np.std(precision_al))
        , 'th': (np.mean(precision_al), np.std(precision_al))}
    result['recall'] = {'so': (np.mean(recall_so), np.std(recall_so)), 'al': (np.mean(recall_al), np.std(recall_al))
        , 'th': (np.mean(recall_th), np.std(recall_th))}
    result['F1'] = {'so': (np.mean(F1_so), np.std(F1_so)), 'al': (np.mean(F1_al), np.std(F1_al)), 'th': (np.mean(F1_th), np.std(F1_th))}

    append_relative_err(result)

    return result



def simu_setting_2_str(p, mode):
    return str(mode)+'_'+str(p)




def simu(num_obs, generating_mode, res_file_name = 'result'):
    result = {}
    for p in [12, 48, 96]:
        for mode in ['ho', 'he']:
            key_name = simu_setting_2_str(p, mode)
            print(key_name)
            sub_res = simu_help(mode, num_obs = num_obs, p=p, generating_mode = generating_mode)
            result[key_name] = sub_res
    with open(os.path.join(RES_DIR, res_file_name), 'wb') as f:
        pickle.dump(result, f)
    return result




def load_result(result_file_name = 'result'):
    print(os.path.join(RES_DIR, result_file_name))
    with open(os.path.join(RES_DIR, result_file_name), 'rb') as handle:
        res = pickle.load(handle)
    return res





def extract_tuple(errs_dict):
    num_obs = len(errs_dict)
    ls = sorted(errs_dict.items())
    freq_ind, values = zip(*ls)
    freq = [index_to_freq(x, num_obs) for x in freq_ind]
    return freq, values





if __name__ == "__main__":
    random.seed(1)
    #simu(400, generating_mode='ma', res_file_name='ma_result_400')
    simu(800, generating_mode='ma', res_file_name='ma_result_800')
    #simu(400, generating_mode = 'var', res_file_name = 'var_result_400')
    #simu(800, generating_mode='var', res_file_name='var_result_800')

    #simu_ma_help(mode = 'ho', num_obs = 600, p=48, graphics=True)