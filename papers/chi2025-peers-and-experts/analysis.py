#!/usr/bin/env python3
"""Run the three experiments using the original statistical functions."""
from pathlib import Path
import ast, contextlib, functools, hashlib, json, logging, os, sys, warnings
import math, itertools, datetime
import numpy as np
import pandas as pd
import scipy
from scipy import stats
from scipy.stats import ttest_ind, ttest_rel, kruskal, f_oneway, pearsonr, sem
import statsmodels
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as font_manager
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.transforms import Bbox
from matplotlib.axes import Axes

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results'
OUT.mkdir(exist_ok=True)
PLAN=json.loads((ROOT/'analysis_code/execution_plan.json').read_text())
CELLS={}
for experiment, entry in PLAN.items():
    source=(ROOT/'analysis_code'/entry['notebook']).read_text()
    CELLS[experiment]={part.split('\n',1)[0]:part.split('\n',1)[1]
                       for part in source.split('# %% analysis block ')[1:]}
SCHEMA=json.loads((ROOT/'data/schema.json').read_text())
warnings.filterwarnings('ignore')  # Same setting as notebook import cells.
logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)

# API-only bridge: old Matplotlib accepted a positional fontdict. No plot data edits.
for method in ['set_xticklabels','set_yticklabels']:
    original=getattr(Axes,method)
    def compat(self, labels, *args, _original=original, **kwargs):
        if args:
            assert len(args)==1 and isinstance(args[0],dict)
            kwargs['fontdict']=args[0]
        return _original(self, labels, **kwargs)
    setattr(Axes,method,compat)

tests=[];boots=[];draws=[];runs=[];model_rows=[]
GLM_FIT=sm.GLM.fit
def execute(e, cell, env, definitions_only=False):
    source=CELLS[str(e)][str(cell)]
    filename=f"{PLAN[str(e)]['notebook']}:cell{cell}"
    env['_source_cell']=cell
    print('\n###',filename)
    tree=ast.parse(source,filename=filename)
    for node in tree.body:
        if definitions_only and not isinstance(node,(ast.FunctionDef,ast.Import,ast.ImportFrom)):
            continue
        if isinstance(node,ast.Expr):
            value=eval(compile(ast.Expression(node.value),filename,'eval'),env)
            if value is not None:
                if isinstance(value,tuple) and any(isinstance(v,np.ndarray) and v.size>20 for v in value):
                    print('Bootstrap arrays saved in bootstrap_draws.csv; returned test:',value[-1])
                else:
                    print(value)
        else:
            exec(compile(ast.Module(body=[node],type_ignores=[]),filename,'exec'),env)
    runs.append({'experiment':e,'cell':cell,'source':filename,'definitions_only':definitions_only})

def install_recorders(e,env):
    def fit_record(self,*args,**kwargs):
        result=GLM_FIT(self,*args,**kwargs)
        model_id=1+len({r['model_id'] for r in model_rows})
        for name,estimate,se,statistic,p in zip(result.params.index,result.params,result.bse,result.tvalues,result.pvalues):
            model_rows.append({'model_id':model_id,'experiment':e,'source_cell':env['_source_cell'],
                               'dependent':self.endog_names,'term':name,'estimate':estimate,'se':se,
                               'statistic':statistic,'p':p,'family':type(self.family).__name__,'n':result.nobs})
        return result
    sm.GLM.fit=fit_record
    name='t_test_helper' if e<3 else 't_test_multi'
    old=env[name]
    @functools.wraps(old)
    def test(df,measure,*groups):
        # Call the unchanged author function; export the same inputs/outputs additionally.
        value=old(df,measure,*groups)
        con,exp=groups if groups else (0,1)
        a=df.query('treatment==@con')[measure];b=df.query('treatment==@exp')[measure]
        result=ttest_ind(a,b)
        tests.append({'experiment':e,'source_cell':env['_source_cell'],'measure':measure,
                      'control':con,'experimental':exp,'n_control':len(a),'n_experimental':len(b),
                      'mean_control':a.mean(),'mean_experimental':b.mean(),
                      'printed_df':len(df)-1,'t':result.statistic,'p':result.pvalue})
        return value
    env[name]=test
    if 'boot_strap' in env:
        original=env['boot_strap']
        @functools.wraps(original)
        def bootstrap(agree,disagree,measurement):
            a,b,test=original(agree,disagree,measurement)
            call=len(boots)+1
            boots.append({'call':call,'experiment':e,'source_cell':env['_source_cell'],
                          'measure':measurement,'n_agree':len(agree),'n_disagree':len(disagree),
                          'mean_agree':np.mean(a),'q05_agree':np.quantile(a,.05),'q95_agree':np.quantile(a,.95),
                          'mean_disagree':np.mean(b),'q05_disagree':np.quantile(b,.05),'q95_disagree':np.quantile(b,.95),
                          'delta':np.mean(a)-np.mean(b),'superiority':np.mean((a-b)>0),
                          'paired_t':test.statistic,'paired_p':test.pvalue})
            draws.extend({'call':call,'replicate':i+1,'agree':x,'disagree':y} for i,(x,y) in enumerate(zip(a,b)))
            return a,b,test
        env['boot_strap']=bootstrap

def read_trials(e):
    combined=pd.read_csv(ROOT/'data/clean_trials.csv')
    x=combined.loc[combined.experiment.eq(e)].sort_values('source_row')
    d=x[list(SCHEMA[str(e)])].copy()
    for col,dtype in SCHEMA[str(e)].items():
        if dtype=='bool':
            d[col]=d[col].map(lambda v:v if isinstance(v,bool) else {'True':True,'False':False}[str(v)])
        else:d[col]=d[col].astype(dtype)
    return d.reset_index(drop=True)

def run_experiment(e):
    plan=PLAN[str(e)]
    env=dict(globals())
    env['valid_predictions_task']=read_trials(e)
    d=env['valid_predictions_task']
    env['valid_predictions_task_agree']=d.query('expert_ai_agreement==1')
    env['valid_predictions_task_disagree']=d.query('expert_ai_agreement==0')
    if e<3:
        x=pd.read_csv(ROOT/'data/trials_with_placebo.csv')
        env['valid_predictions']=x.loc[x.experiment.eq(e)].drop(columns='experiment').reset_index(drop=True)
    env['survey']=pd.read_csv(ROOT/'data'/f'exp{e}_survey.csv')
    env['expertise_survey']=pd.read_csv(ROOT/'data'/f'exp{e}_expertiseSurvey.csv')
    np.random.seed(42)  # Exact seed from the original import cell; fresh kernel per experiment.
    for cell in plan['definitions']:execute(e,cell,env,True)
    install_recorders(e,env)
    execute(e,plan['summary'],env)
    env['res'].to_csv(OUT/f'exp{e}_participant_summary.csv',index=False)
    for cell in plan['tests']+plan['models']:execute(e,cell,env)
    if e<3:
        # The author's sharing-model invocation is preserved as a commented line
        # in the same cell as the accuracy model. Re-enable that exact invocation.
        cell=159 if e==1 else 85
        line=next(line for line in CELLS[str(e)][str(cell)].splitlines()
                  if line.startswith('# mediation(valid_predictions_task,"finalWill"'))
        env['_source_cell']=cell
        print('\n### Original commented sharing invocation, re-enabled:',line)
        exec(line[2:],env)
        runs.append({'experiment':e,'cell':cell,'source':'original commented sharing invocation','definitions_only':False})
    else:
        # Use the same author ANOVA helper and input units for all five figure-5 outcomes.
        # This is launcher orchestration; the helper itself is unchanged.
        env['_source_cell']='55 (launcher calls)'
        for frame,measure in [(d.query('label==1'),'finalWill'),(d.query('label==0'),'finalWill'),
                              (env['res'],'willingness_discernment')]:
            print('\n### Original anova_test helper:',measure)
            env['anova_test'](frame,measure)
    for cell in plan['bootstrap']:execute(e,cell,env)
    for cell in plan['plots']:
        plt.close('all')
        execute(e,cell,env)
        # Two appendix cells define their plotting function without calling it.
        if (e,cell) in [(1,224),(2,185)]:env['bar_vis_appendix']()
        for i,num in enumerate(plt.get_fignums()):
            fig=plt.figure(num)
            fig.savefig(OUT/f'exp{e}_cell{cell}_{i+1}.png',dpi=45,bbox_inches='tight')
        plt.close('all')

def main():
    for p in ['generated_images/experiment1','generated_images/experiment2','generated_images/experiment3',
              'generated_images_230826/experiment3']:(OUT/p).mkdir(parents=True,exist_ok=True)
    os.chdir(OUT)
    for e in [1,2,3]:
        print(f'Running original experiment {e} cells...',flush=True)
        with (OUT/f'exp{e}_log.txt').open('w',buffering=1) as log, contextlib.redirect_stdout(log):
            run_experiment(e)
    pd.DataFrame(tests).to_csv(OUT/'t_tests.csv',index=False)
    pd.DataFrame(boots).to_csv(OUT/'bootstrap_summary.csv',index=False)
    pd.DataFrame(draws).to_csv(OUT/'bootstrap_draws.csv',index=False)
    pd.DataFrame(runs).to_csv(OUT/'executed_cells.csv',index=False)
    pd.DataFrame(model_rows).to_csv(OUT/'Python_coefficients.csv',index=False)
    versions={'python':sys.version,'numpy':np.__version__,'pandas':pd.__version__,
              'scipy':scipy.__version__,'statsmodels':statsmodels.__version__,'matplotlib':matplotlib.__version__,
              'pythonhashseed':os.environ.get('PYTHONHASHSEED'),'numpy_seed_per_experiment':42}
    (OUT/'python_environment.json').write_text(json.dumps(versions,indent=2))
    print('Original Python cells completed.',flush=True)

if __name__=='__main__':main()
