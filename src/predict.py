import numpy as np
import joblib
import pickle
import pandas as pd

from pathlib import Path

# Original frequencies format
orig_col = ['500k', '1k', '2k', '3k', '4k', '6k', '8k']

# Model Path
m_path = Path.cwd() / 'src' / 'model'

# Load required files
with open(m_path / 'models.pkl', 'rb') as f:
    pickle_models = pickle.load(f)

def get_closer_5_multi(n):
    """
    Get the closest 5 multiple
    input:  number (float)
    output: number (int)
    """
    r = n % 5
    r = n+(5-r) if r>=2.5 else n-r
    return int(r)

def find_audio_model(comb):
    """
    Find the ML model to given frequency combination
    input:  comb (Frequencies combination)
    output: x (Frequencies to analyze)
            y (Target frequency)
            model_name (Model name)
    """
    for model in pickle_models:
        x, y, model_name = [model['x'], model['y'], model['model_name']]
        if len(comb)!=len(x):continue
        if all((i in x) for i in comb):
            return x, y, model_name
    
    return None

def get_predictions(_input):
    """
    Get prediction from given values
    input:  _input (Frequencies names and values)
    output: predicted frequencies
    """
    comb, freqs = _input
    comb_s = len(comb)
    preds = []
    for i in range(comb_s, 7):
        model_inf = find_audio_model(comb)
        if model_inf:
            x, y, model_name = find_audio_model(comb)
        else:
            return None
        model = joblib.load(m_path / model_name)
        pred = get_closer_5_multi(model.predict(np.array([freqs]))[0])
        comb += [y]
        freqs += [pred]
        
    orig_idx = [orig_col.index(i) for i in comb]
    res = [i for _,i in sorted(zip(orig_idx,freqs))]
    return res