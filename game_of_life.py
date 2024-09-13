# Build streamlit app for game of life
import base64
import os.path

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from matplotlib import colors
from matplotlib.animation import PillowWriter
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode

from game_of_life_module import GameOfLife

# Set up the game of life
if "game" not in st.session_state:
    game = GameOfLife(randomize=False)
    st.session_state.game = game
else:
    game = st.session_state.game

# game.randomize()

# Use entire page width
st.set_page_config(layout="wide")

# Set up the plot
fig, ax = plt.subplots()
cmap = colors.ListedColormap(["white", "black"])

checkbox_renderer = JsCode(
    """
class CheckboxRenderer{

    init(params) {
        this.params = params;

        this.eGui = document.createElement('input');
        this.eGui.type = 'checkbox';
        this.eGui.checked = params.value;

        this.checkedHandler = this.checkedHandler.bind(this);
        this.eGui.addEventListener('click', this.checkedHandler);
    }

    checkedHandler(e) {
        let checked = e.target.checked;
        let colId = this.params.column.colId;
        this.params.node.setDataValue(colId, checked);
    }

    getGui(params) {
        return this.eGui;
    }

    destroy(params) {
    this.eGui.removeEventListener('click', this.checkedHandler);
    }
}//end class
"""
)


# # Set up the animation
def animate(i):
    game.life_epoch()
    ax.imshow(game.current_state, cmap=cmap, animated=True)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    # ax.axis('off')


if not os.path.isfile("Intro_gif.gif"):
    game.randomize()
    ani = animation.FuncAnimation(fig, animate, frames=50, interval=100)

    with st.spinner("Preparing animation..."):
        # components.html(ani.to_jshtml(), height=550)
        ani.save("media/Intro_gif.gif", writer=PillowWriter())
        # ani.save("GameOLife.gif", writer=PillowWriter())


# Set up the streamlit app
st.title("Game of Life")

# file_ = open(r"D:\CSM\Mines_Research\Repositories\exploring_dask\Intro_gif.gif", "rb")
file_ = open(r"media/Intro_gif.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
    unsafe_allow_html=True,
)

st.write(
    "Conway's Game of Life is a cellular automaton devised by the British mathematician John Horton Conway in 1970. It is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. One interacts with the Game of Life by creating an initial configuration and observing how it evolves."
)

st.write(
    "The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, live or dead. Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent."
)

st.write(
    "The initial pattern constitutes the seed of the system. The first generation is created by applying the above rules simultaneously to every cell in the seed — births and deaths occur simultaneously - , and the discrete moment at which this happens is sometimes called a tick (in other words, each generation is a pure function of the preceding one). The rules continue to be applied repeatedly to create further generations."
)

st.write(
    "The video above shows an instance of the game of life. The app below can be used to generate generations of an input initial state one at a time or as an animation."
)

st.sidebar.title("Rules")
st.sidebar.write("At each step in time, the following transitions occur:")
st.sidebar.write(
    "1. Any live cell with fewer than two live neighbours dies, as if by underpopulation."
)
st.sidebar.write(
    "2. Any live cell with two or three live neighbours lives on to the next generation."
)
st.sidebar.write(
    "3. Any live cell with more than three live neighbours dies, as if by overpopulation."
)
st.sidebar.write(
    "4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction."
)

st.sidebar.title("Legend")
st.sidebar.write("White or 0: Dead cell")
st.sidebar.write("Black or 1: Live cell")

# Set up columns for input
c1, c2 = st.columns((1, 2))

# Set up for controling states and animation
f1, f2, f3 = st.columns((3, 2, 3))

f3.header("Current State")
f1.header("Previous State")
f2.header("Controls")


with c1:
    container = st.container(border=True)
    row_size = container.slider("Row Size", 10, 100, 10)
    game.rows = row_size
    st.session_state.game = game
    column_size = container.slider("Column Size", 10, 100, 10)
    game.columns = column_size
    st.session_state.game = game
    prob = container.slider("Probability of 1s", 0.0, 1.0, 0.5)
    game.prob = prob
    st.session_state.game = game
    container.write("Create initial state that can be edited by clicking grid")
    init_state = container.radio(
        "Intialize with", ["Random", "zeros", "ones"], index=None
    )

    if init_state in ["Random", "zeros", "ones"] or "init_flag" in st.session_state:
        if container.button("Initialize") and init_state in ["Random", "zeros", "ones"]:
            if init_state == "Random":
                game.randomize()
                st.session_state.game = game
                st.session_state.init_flag = 1
                del st.session_state["ag"]
            elif init_state == "zeros":
                game.current_state = np.zeros((row_size, column_size), dtype=int)
                st.session_state.game = game
                st.session_state.init_flag = 1
                del st.session_state["ag"]
            elif init_state == "ones":
                game.current_state = np.ones((row_size, column_size), dtype=int)
                st.session_state.game = game
                st.session_state.init_flag = 1
                del st.session_state["ag"]
        with c2:
            if "ag" in st.session_state:
                ag = st.session_state.ag
                df = ag["data"]
                # game.current_state = np.array(ag['data'], dtype=int)
            else:
                # c12.write(game.current_state)
                df = pd.DataFrame.from_records(np.array(game.current_state, dtype=bool))
                df.columns = [str(a) for a in df.columns]

            gb = GridOptionsBuilder.from_dataframe(df)
            for col in df.columns:
                gb.configure_column(col, editable=True, cellRenderer=checkbox_renderer)

            # st.write('#### interface')
            ag = AgGrid(
                df,
                gridOptions=gb.build(),
                fit_columns_on_grid_load=True,
                update_mode=GridUpdateMode.MANUAL,
                allow_unsafe_jscode=True,
                enable_enterprise_modules=False,
                theme="alpine",
            )
            st.session_state.ag = ag

if c1.button("Accept Initial State"):
    game.current_state = np.array(ag["data"], dtype=int)
    fig, ax = plt.subplots()
    ax.imshow(game.current_state, cmap=cmap)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    f3.pyplot(fig, clear_figure=False)


# # Set up the next button
if f2.button("Next State"):
    fig, ax = plt.subplots()
    ax.imshow(game.current_state, cmap=cmap)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    f1.pyplot(fig, clear_figure=False)

    game.life_epoch()
    fig, ax = plt.subplots()
    ax.imshow(game.current_state, cmap=cmap)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    f3.pyplot(fig, clear_figure=False)


with f2.container(border=True):
    # st.title('For Animation')
    frames = st.slider("Number of iterations", 10, 100, 10)
    Speed = st.slider("Speed", 1, 100, 50)
    if st.button("Animate"):
        fig, ax = plt.subplots()
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        ani = animation.FuncAnimation(fig, animate, frames=frames, interval=Speed)

        with st.spinner("Preparing animation..."):
            # components.html(ani.to_jshtml(), height=550)
            # ani.save('D:\CSM\Mines_Research\Repositories\exploring_dask\GameOLife.gif', writer=PillowWriter())
            ani.save("media/Current_GameOLife.gif", writer=PillowWriter())

        file_ = open("media/Current_GameOLife.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()

        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
            unsafe_allow_html=True,
        )

# Set up the socials
b1, b2, b3 = st.columns(3)
b1.write("Author: Hafiz Issah")
b2.info("**[Email](mailto:aissah@gmail.com)**", icon="✉️")
b3.info("**[GitHub](https://github.com/aissah)**", icon="💻")
