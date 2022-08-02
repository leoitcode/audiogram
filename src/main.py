import streamlit as st
from predict import get_predictions
import pandas as pd

# Original frequencies format
orig_col = ['500k', '1k', '2k', '3k', '4k', '6k', '8k']

if __name__ == "__main__":
    st.title("AUDIOGRAM PREDICT")
    st.markdown("Input values dB (Decibels) for frequencies (2k, 4k, 6k)")
    _2k_freq = st.number_input("2k", value=0, step=5, min_value=-5, max_value=95)
    _4k_freq = st.number_input("4k", value=0, step=5, min_value=-5, max_value=95)
    _6k_freq = st.number_input("6k", value=0, step=5, min_value=-5, max_value=95)

    comb = ['2k','4k','6k']
    freqs = [_2k_freq, _4k_freq, _6k_freq]
    try:
        freqs = list(map(float, freqs))
    except:
        st.write('Wrong input')

    new_freq = st.checkbox('Add a new frequency?')
    if new_freq:
        freq_value = st.number_input("Value", value=0, step=5, min_value=-5, max_value=95)
        freq_name = st.selectbox("Frequency:", ('500k','1k','3k','8k'))
        comb.append(freq_name)
        try:
            freqs.append(float(freq_value))
        except:
            st.write('Wrong input')

    _input = (comb, freqs)
    if all(freqs):
        preds = [int(i) for i in get_predictions(_input)]
        if preds:
            data = {}
            for i,c in enumerate(orig_col):
                data[c] = [preds[i]]
            df_res = pd.DataFrame(data)
            st.subheader('Results:')
            st.dataframe(df_res)
        else:
            st.write('Wrong input')