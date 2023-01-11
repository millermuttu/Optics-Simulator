import streamlit as st
import numpy as np
import math
import matplotlib.pyplot as plt
from PIL import Image
# from numericalunits import nm, mm, cm
from streamlit.components.v1 import html
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.add_vertical_space import add_vertical_space
from annotated_text import annotated_text, annotation

######################## functions #####################################
@st.cache
def closest_value(input_list, input_value):
    arr = np.asarray(input_list)
    i = (np.abs(arr - input_value)).argmin()
    return arr[i]
########################################################################

st.session_state.update(st.session_state)
st.title(":blue[Grating Specification:]")
add_vertical_space(3)


with st.sidebar:
    st.subheader("Please input the Grating Specification...")

user_input = st.container()
groove_list = [300,600,1200,1800,2400]

if 'page_1' not in st.session_state:
    st.session_state.page_1 = {
        'continue_btn_state' : True,
        'N_user_input': 0.0,
        'blaze_angle_input': 17.0
    }
    st.session_state.span = 0.0
    st.session_state.N = 0.0
    st.session_state.blaze_wavelength = 0.0
    st.session_state.N = 0.0
    st.session_state.D = 0.0
    st.session_state.blaze_angle_calculated = 0.0
    st.session_state.m = 1
    

st.session_state.span = st.session_state['span_end']-st.session_state['span_start']
st.session_state.blaze_wavelength = (st.session_state['span_end']+st.session_state['span_start'])/2
st.session_state.N_calculated = st.session_state.blaze_wavelength/st.session_state.spectral_resolution
st.session_state.N = closest_value(groove_list, st.session_state.N_calculated)


with user_input:

    annotated_text(
    annotation(f"The entered Spectral Resolution is {st.session_state['spectral_resolution']} nm \
                with span of {st.session_state.span} nm",background='#DBF9DB', color="black", 
                border="1px solid red",
                )
    )
    add_vertical_space(1)
    # st.info(f"The entered Spectral Resolution is {st.session_state['spectral_resolution']} nm \
    #             with span of {st.session_state.span} nm", icon="ℹ️")

    st.warning(f"According to your input the calculated Number of grooves per mm for the grating is {st.session_state.N},\
                the standard grating grooves are 300, 600, 1200, 1800, 2400.\
                we would recomend using {st.session_state.N}\
                please change if you wish by using below dropdown", icon="⚠️")
    st.selectbox(label="_Please change the N value if you wish to (Grooves/mm)_",
                 options=groove_list,
                 key='N_input',
                 index=groove_list.index(st.session_state.N))

    ## calculate the "D" the distance between two holes in grating
    st.session_state.D = 1/st.session_state.N_input

    ## calculate the blaze angle  (arcsin(m*blaze_eavelength/2*D))
    st.session_state.blaze_angle_calculated = np.round(np.arcsin((st.session_state.m*st.session_state.blaze_wavelength*(1e-9))/(2*st.session_state.D*(1e-3)))*180/np.pi,2)

    # annotated_text(
    # annotation(f"For the selected N values of grating, calculated blaze angle based on blaze wavelength of \
    #         {st.session_state.blaze_wavelength}nm is {st.session_state.blaze_angle_calculated}. Please note \
    #             that this blaze angle is for littrow configureation",background='white', color="black", 
    #             border="1px solid red",
    #             )
    # )
    # add_vertical_space(1)

    st.info(f"For the selected N values of grating, calculated blaze angle based on blaze wavelength of \
            :green[{st.session_state.blaze_wavelength}]nm is :green[{st.session_state.blaze_angle_calculated}]. Please note \
                that this blaze angle is for littrow configureation", icon="ℹ️")

    st.number_input(label="_Please change the blaze angle if required_",
                  value=st.session_state.page_1['blaze_angle_input'],
                  min_value=5.0,
                  max_value=35.0,
                  key='blaze_angle')
    continue_btn = st.button("Continue", help="Click to sumbit and navigate to next page")

    if continue_btn:
        st.session_state.N = st.session_state.N_input
        st.session_state.page_1['blaze_angle_input'] = st.session_state.blaze_angle
        switch_page("final result")
