import os
import sys
import pickle
from subprocess import call
RES_DIR='./result'
TABLE_DIR='table'

'''
\begin{table}[p]
\def~{\hphantom{0}}
\tbl{RMISE (in $10^{-2}$) Under Homogeneous Setting}{%
\begin{tabular}{l@{\hskip 0.4in}ccccc}
%\\
 \\
 & Smoothed   & Shrinkage& Hard Threshold  & Lasso & Adaptive Lasso\\
 \\
 VMA & & & & &\\
 p = 12 & & & & &\\
 \multicolumn{1}{r}{n = 400}  & 20.71(2.04) & 14.54(0.94) & 13.88(1.65)  & 13.24(1.33) & \textbf{12.02}(1.36)\\
  \multicolumn{1}{r}{n = 800}  & 13.57(0.85) & 10.60(0.54) & \textbf{6.19}(0.96) & 8.48(0.88) & 6.26(0.85)\\
 p = 48 & & & & &  \\
 \multicolumn{1}{r}{n = 400}  & 81.15(2.77) & 25.18(0.35) & 24.39(0.79) & 20.77(0.91) &\textbf{18.27}(0.80)\\
  \multicolumn{1}{r}{n = 800}  & 54.72(1.47) &21.65(2.35) &11.58(0.57)  & 13.44(0.51) &\textbf{9.26}(0.48)\\
 p = 96 & & & & &  \\
 \multicolumn{1}{r}{n = 400}  & 161.76(3.87)& 28.88(0.27) & 29.05(0.47) & 26.02(0.55) & \textbf{22.74}(0.52)\\
  \multicolumn{1}{r}{n = 800}  & 108.45(1.75)&26.25(0.22) &15.53(0.48)  &16.90(0.40) &\textbf{11.87}(0.38)\\
 \\
 VAR & &  &  &  & \\
 p = 12 & & & & &  \\
 \multicolumn{1}{r}{n = 400}  &28.93(1.98) &\textbf{3.91}(0.53) &5.13(0.74) & 11.44(0.93) & 6.56(0.79) \\
  \multicolumn{1}{r}{n = 800}  & 19.36(1.05) & \textbf{3.16}(0.22)& 3.89(0.34)& 7.99(0.50) & 4.55(0.35)\\
 p = 48 & & & & &\\
 \multicolumn{1}{r}{n = 400}  &114.32(2.67)&\textbf{4.36}(0.36) &5.75(0.57)  & 16.58(0.51) & 7.97(0.47) \\
  \multicolumn{1}{r}{n = 800}  &77.64(1.59) & \textbf{3.51}(0.19)& 3.81(0.13)  &11.23(0.38) & 4.93(0.20)\\
 p = 96 & & & & & \\
 \multicolumn{1}{r}{n = 400}  & 229.78(3.59)& \textbf{4.58}(0.35)& 6.42(0.41) & 19.42(0.33) & 9.02(0.30) \\
  \multicolumn{1}{r}{n = 800}  & 154.02(2.05)& \textbf{3.58}(0.18)&3.83(0.12) & 13.25(0.28) & 5.29(0.17)\\
\end{tabular}}
\label{table:rmise-homogeneous}
\begin{tabnote}
\end{tabnote}
\end{table}
'''


def load_result(result_file_name ):
    print(os.path.join(RES_DIR, result_file_name))
    with open(os.path.join(RES_DIR, result_file_name), 'rb') as handle:
        res = pickle.load(handle)
    return res


def test_structure():
    result_name = '_'.join(['ma', 'result', str(400)])
    print(result_name)
    res = load_result(result_name)
    print(list(res.keys()))
    print("=======")
    print(list(res['ho_12'].keys()))
    print("=========")
    print(list(res['ho_12']['error'].keys()))


def write_rmise_header_tail(file_name):
    call('rm -f temp', shell=True)
    call('touch temp && cat rmise_header >> temp && cat {0} >> temp && mv temp {0}'.format(file_name), shell=True)
    call('touch temp && cat {0} >> temp && cat rmise_tail >> temp  && mv temp {0}'.format(file_name), shell=True)



def tuple_2_string(my_tuple):
    return str(round(my_tuple[0]*100,2))+'('+str(round(my_tuple[1]*100,2))+')'



def extract_array_result(result, model_type, p):
    sub_result = result[model_type + '_' + str(p)]
    sm = '&' + tuple_2_string(sub_result['relative_error']['sm'])
    sh = '&' + tuple_2_string(sub_result['relative_error']['sh'])
    th = '&' + tuple_2_string(sub_result['relative_error']['th'])
    so = '&' + tuple_2_string(sub_result['relative_error']['so'])
    al = '&' + tuple_2_string(sub_result['relative_error']['al'])
    return sm+sh+th+so+al




def write_vma(file_handle, model_type='ho'):
    result_file_name = 'ma_result_400'
    result_400 = load_result(result_file_name)
    result_file_name = 'ma_result_800'
    result_800 = load_result(result_file_name)
    file_handle.write('VMA & & & & &\\\\\n')
    for p in [12,48,96]:
        file_handle.write('p = {} & & & & &\\\\\n'.format(p))
        for n in [400, 800]:
            result = eval('result_'+str(n))
            file_handle.write('\\multicolumn{{1}}{{r}}{{n = {0}}}'.format(str(n)))
            file_handle.write(extract_array_result(result, model_type, p)+'\\\\\n')



def write_var(file_handle, model_type='ho'):
    result_file_name = 'ma_result_400'
    result_400 = load_result(result_file_name)
    result_file_name = 'ma_result_800'
    result_800 = load_result(result_file_name)
    file_handle.write('VAR & & & & &\\\\\n')
    for p in [12, 48, 96]:
        file_handle.write('p = {} & & & & &\\\\\n'.format(p))
        for n in [400, 800]:
            result = eval('result_' + str(n))
            file_handle.write('\\multicolumn{{1}}{{r}}{{n = {0}}}'.format(str(n)))
            file_handle.write(extract_array_result(result, model_type, p) + '\\\\\n')


def write_rmise_table(model_type='ho'):
    file_name = 'rmise_'+model_type+'_table'
    with open(os.path.join(RES_DIR, 'table', file_name), 'w') as table_handle:
        write_vma(table_handle, model_type)
        write_var(table_handle, model_type)
    write_rmise_header_tail(os.path.join(RES_DIR, 'table', file_name))




if __name__ == "__main__":
    write_rmise_table(model_type='ho')
    write_rmise_table(model_type='he')
