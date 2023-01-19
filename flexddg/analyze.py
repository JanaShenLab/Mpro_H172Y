import sqlite3
import pandas as pd
import sys
import numpy as np

case_name = 1
trajectory_stride = 1
struct_number = 1

def readDb3(filename):
    conn = sqlite3.connect(filename)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    num_batches = c.execute('SELECT max(batch_id) from batches').fetchone()[0]
    scores = pd.read_sql_query('''
        SELECT batches.name, structure_scores.struct_id, score_types.score_type_name, structure_scores.score_value, score_function_method_options.score_function_name from structure_scores
        INNER JOIN batches ON batches.batch_id=structure_scores.batch_id
        INNER JOIN score_function_method_options ON score_function_method_options.batch_id=batches.batch_id
        INNER JOIN score_types ON score_types.batch_id=structure_scores.batch_id AND score_types.score_type_id=structure_scores.score_type_id
        ''', conn)
    def renumber_struct_id( struct_id ):
            return trajectory_stride * ( 1 + (int(struct_id-1) // num_batches) )

    scores['struct_id'] = scores['struct_id'].apply( renumber_struct_id )
    scores['name'] = scores['name'].apply( lambda x: x[:-9] if x.endswith('_dbreport') else x )
    scores = scores.pivot_table( index = ['name', 'struct_id', 'score_function_name'], columns = 'score_type_name', values = 'score_value' ).reset_index()
    scores.rename( columns = {
        'name' : 'state',
        'struct_id' : 'backrub_steps',
    }, inplace=True)
    scores['struct_num'] = struct_number
    scores['case_name'] = case_name
    conn.close()
    return(scores)


if(__name__=='__main__'):
    if(len(sys.argv)<2):
        print('Usage: {} file1.db3 file2.db3 ...'.format(sys.argv[0]))
        sys.exit()

    dG_apo = []
    dG_holo= []
    for f in sys.argv[1:]:
        scores = readDb3(f)
        dG_apo.append(scores.loc[scores['state']=='unbound_mut']['total_score'].values[0] - scores.loc[scores['state']=='unbound_wt']['total_score'].values[0])
        dG_holo.append(scores.loc[scores['state']=='bound_mut']['total_score'].values[0] - scores.loc[scores['state']=='bound_wt']['total_score'].values[0])

    print('dG_apo : {:.2f} +/- {:.2f}'.format(np.mean(dG_apo),np.std(dG_apo)/np.sqrt(len(dG_apo))))
    print('dG_holo : {:.2f} +/- {:.2f}'.format(np.mean(dG_holo),np.std(dG_holo)/np.sqrt(len(dG_holo))))
