import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io


def random_surface(seed):
    return [np.random.uniform(-2, 2), # amp x
            np.random.uniform(-2, 2), # amp y
            np.random.uniform(-0.5, 0.9), # freq x
            np.random.uniform(-0.5, 0.9),  # freq y
            np.random.uniform(0, 2 * np.pi)]  # phase

def create_surface(amp_x, amp_y, freq_x, freq_y, phase):
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    x, y = np.meshgrid(x, y)
    z = np.zeros_like(x)
    for i in range(10):
        amp_x = amp_x # np.random.uniform(-2, 2)
        amp_y = amp_y # np.random.uniform(-2, 2)
        freq_x = freq_x # np.random.uniform(-0.5, 0.9)
        freq_y = freq_y # np.random.uniform(-0.5, 0.9)
        phase = phase # np.random.uniform(0, 2 * np.pi)
        z += amp_x * np.sin(freq_x * x + phase) + amp_y * np.cos(freq_y * y + phase)

    # plot 3D surface 10x10
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_wireframe(x, y, z, rstride=0, cstride=1, linewidth=0.3, color=fig_color)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.axis('off')
    # ax.view_init(azim=30, elev=60) # set viewing angle
    ax.margins(0, 0, 0)  # remove margins
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)  # adjust figure size
    return fig


#@st.cache_data(ttl=3600)
def random_spiro(seed):
    return [np.random.randint(1, 200), # R
            np.random.randint(1, 200), # r
            np.random.randint(1, 200), # d
            np.random.randint(1, 10),  # freq1
            np.random.randint(1, 10),  # freq2
            np.random.randint(1, 500), # amp1
            np.random.randint(1, 500), # amp2
            np.random.randint(1, 20)] # k


#@st.cache_data(ttl=3600) # clear cache after 1h
def create_spiro(R, r, d, freq1, freq2, amp1, amp2, k):
    fig, ax = plt.subplots(figsize=(10, 10))

    R = R # big circle radius
    r = r # # small circle radius
    d = d # distance from the center of the small circle to the tracing point
    freq1 = freq1  # frequency of first sine wave
    freq2 = freq2  # frequency of second sine wave
    amp1 = amp1  # amplitude of first sine wave
    amp2 = amp2  # amplitude of second sine wave
    k = np.pi / k  # coefficient to adjust the shape of the pattern
    theta = np.linspace(0, 60 * np.pi, 10000)

    # x and y equations with sine and cosine waves
    x = (R - r) * np.cos(theta) + d * np.cos((R - r) / r * theta) + k * amp1 * np.sin(
        freq1 * theta) + k * amp2 * np.cos(freq2 * theta)
    y = (R - r) * np.sin(theta) - d * np.sin((R - r) / r * theta) + k * amp1 * np.cos(
        freq1 * theta) - k * amp2 * np.sin(freq2 * theta)

    ax.plot(x, y, linewidth=0.5, color=fig_color)

    ax.axis('equal')
    ax.axis('off')
    # print("run create_spiro")
    return fig




st.header("Geometrikos")
st.subheader("Create beautiful geometric figures")

# invert colours
invert_button = st.checkbox("Invert colours")
if invert_button:
    fig_color = "white"
    plt.style.use('dark_background')
else:
    fig_color = "black"
    plt.style.use('default')


tab1, tab2 = st.tabs(["Spirograph", "Surface"])



# SPIROGRAPH
with tab1:

    spiro_button = st.button("Create new Spirograph", use_container_width=True, key="spiro_button")
    if spiro_button:
        # create random figure when this button is pressed
        spiro_values = random_spiro(np.random.random())
        # and transfer random values to session state
        st.session_state.spiro = spiro_values
    else:
        # on first run: display default figure
        spiro_values = [1, 71, 192, 4, 4, 100, 74, 4]

    # on first run: initialise session state
    if 'spiro' not in st.session_state:
        st.session_state.spiro = spiro_values

    # st.text(f"spiro_values: {spiro_values}")
    # st.text(f"session state: {st.session_state.spiro}")

    # plot figure with values in session state - * unpacks list into separate values
    fig_spiro = create_spiro(*st.session_state.spiro)
    st.pyplot(fig_spiro)

    # save image for download button
    img = io.BytesIO()
    plt.savefig(img, format='png')

    download_button = st.download_button(
        label="Download Image",
        data=img,
        file_name='image.png',
        mime="image/png",
        use_container_width=True
    )

    # button for testing
    modify_spiro = st.checkbox("Show Menu to modify Spirograph")
    if modify_spiro:
        st.text(f"spiro_values: {spiro_values}")
        st.text(f"session state: {st.session_state.spiro}")

        slider = st.slider("Big circle radius: ", 0, 200, value=st.session_state.spiro[0])
        print(f"slider: {slider}")
        #st.session_state.spiro[0] = slider
        #print(f"session state [0]: {st.session_state.spiro[0]}")
        # update figure

        # # show slider menu
        # st.session_state.spiro[0] = st.slider('Big circle radius: ', 0, 200, value=st.session_state.spiro[0]) # R
        # st.session_state.spiro[1] = st.slider('Small circle radius: ', 1, 200, value=st.session_state.spiro[1]) # r
        # st.session_state.spiro[2] = st.slider('Distance: ', 0, 200, value=st.session_state.spiro[2]) # d
        # st.session_state.spiro[3] = st.slider('Frequency 1st wave: ', 0, 10, value=st.session_state.spiro[3]) # freq1
        # st.session_state.spiro[4] = st.slider('Frequency 2nd wave: ', 0, 10, value=st.session_state.spiro[4]) # freq2
        # st.session_state.spiro[5] = st.slider('Amplitude 1st wave: ', 0, 500, value=st.session_state.spiro[5]) # amp1
        # st.session_state.spiro[6] = st.slider('Amplitude 2nd wave: ', 0, 500, value=st.session_state.spiro[6]) # amp2
        # st.session_state.spiro[7] = st.slider('Coefficient: ', 1, 25, value=st.session_state.spiro[7])  # k



# SURFACE
with tab2:
   surface_button = st.button("Create new Surface", use_container_width=True, key="surface_button")
   if surface_button:
       # create random figure when this button is pressed
       surface_values = random_surface(np.random.random())
       # and transfer random values to session state
       st.session_state.surface = surface_values
   else:
       # on first run: display default figure
       surface_values = [-0.87, 0.45, 0.54, -0.015, 0.05]

   # on first run: initialise session state
   if 'surface' not in st.session_state:
       st.session_state.surface = surface_values


   # plot figure with values in session state - * unpacks list into separate values
   fig_surface = create_surface(*st.session_state.surface)
   st.pyplot(fig_surface)

   # save image for download button
   img = io.BytesIO()
   plt.savefig(img, format='png')

   download_button = st.download_button(
       label="Download Image",
       data=img,
       file_name='image.png',
       mime="image/png",
       use_container_width=True
   )

   # button for testing
   modify_surface = st.checkbox("Show Menu to modify Surface")
   if modify_surface:
       st.text(f"surface_values: {surface_values}")
       st.text(f"session state: {st.session_state.surface}")

