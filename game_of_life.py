# Build streamlit app for game of life
import base64
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors
from game_of_life_module import GameOfLife
from matplotlib.animation import PillowWriter
import os.path
import pandas as pd
import streamlit.components.v1 as components
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode

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
# cmap = colors.ListedColormap(['black', 'white'])
cmap = colors.ListedColormap(['white','black'])
# ax.imshow(game.current_state, cmap=cmap)
# ax.axis('off')

checkbox_renderer = JsCode("""
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
""")

# # Set up the animation
def animate(i):
    # game.update(i)
    game.life_epoch()
    ax.imshow(game.current_state, cmap=cmap, animated=True)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    # ax.axis('off')

# fig = plt.figure(figsize=(6, 6))

if not os.path.isfile('GameOLife.gif'):
    ani = animation.FuncAnimation(fig, animate, frames=20, interval=100)

    with st.spinner("Preparing animation..."):
        # components.html(ani.to_jshtml(), height=550)
        # ani.save('D:\CSM\Mines_Research\Repositories\exploring_dask\GameOLife.gif', writer=PillowWriter())
        ani.save('GameOLife.gif', writer=PillowWriter())


# df = pd.DataFrame.from_records(np.array(game.current_state, dtype=bool))
# df.columns = [str(a) for a in df.columns]

# # st.write('#### init data')
# # st.dataframe(df)

# gb = GridOptionsBuilder.from_dataframe(df)
# for col in df.columns:
#     gb.configure_column(col, editable=True, cellRenderer=checkbox_renderer)


# st.write('#### interface')
# ag = AgGrid(
#     df, 
#     gridOptions=gb.build(),
#     fit_columns_on_grid_load=True,
#     update_mode=GridUpdateMode.MANUAL,
#     allow_unsafe_jscode=True,
#     enable_enterprise_modules=False,
#     theme='alpine',
# )

# with st.spinner("Preparing animation..."):
    #     animation.save('files/pendulum.gif', writer=PillowWriter())
    # st.image("files/pendulum.gif")

# ani.save('D:\CSM\Mines_Research\Repositories\exploring_dask\GameOLife.gif', writer='imagemagick')
# ani.save('GameOLife.gif', writer='pillow')

# Set up the streamlit app
st.title('Game of Life')

file_ = open("D:\CSM\Mines_Research\Repositories\exploring_dask\GameOLife.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
    unsafe_allow_html=True,
)

st.write('Conway\'s Game of Life is a cellular automaton devised by the British mathematician John Horton Conway in 1970. It is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. One interacts with the Game of Life by creating an initial configuration and observing how it evolves.')

st.write('The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, live or dead. Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent. At each step in time, the following transitions occur:')
st.write('1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.')
st.write('2. Any live cell with two or three live neighbours lives on to the next generation.')
st.write('3. Any live cell with more than three live neighbours dies, as if by overpopulation.')
st.write('4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.')

st.write('The initial pattern constitutes the seed of the system. The first generation is created by applying the above rules simultaneously to every cell in the seed—births and deaths occur simultaneously, and the discrete moment at which this happens is sometimes called a tick (in other words, each generation is a pure function of the preceding one). The rules continue to be applied repeatedly to create further generations.')

st.write('The app below shows the game of life in action. The grid is updated every 50 milliseconds. You can also change the initial state of the grid by clicking on the cells.')


# with st.spinner("Preparing animation..."):
#     components.html(ani.to_jshtml(), height=1000)

# plt.show()


# st.image('D:\CSM\Mines_Research\Repositories\exploring_dask\GameOLife.gif')
# st.pyplot(ani._fig, clear_figure=False)

# Set up the controls
st.sidebar.title('Controls')
st.sidebar.write('You can change the initial state of the grid by clicking on the cells.')
st.sidebar.write('You can also change the size of the grid below.')

# Set up the grid size slider
# row_size = st.sidebar.slider('Row Size', 10, 100, 10)
# column_size = st.sidebar.slider('Column Size', 10, 100, 10)
# prob = st.sidebar.slider('Probability of 1s', 0.0, 1.0, 0.5)

# current_state = np.random.choice([0, 1], (row_size, column_size), p=[1-prob, prob])
# fig, ax = plt.subplots()
# cmap = colors.ListedColormap(['black', 'white'])
# ax.imshow(current_state, cmap=cmap)
# ax.axis('off')
# ani = animation.FuncAnimation(fig, animate, frames=100, interval=50)
# st.pyplot(ani._fig, clear_figure=False)


# current_state = np.random.choice([0, 1], (row_size, column_size), p=[1-prob, prob])
# st.write(game.current_state)


c1, c2 = st.columns((1, 2))

# d1, d2 = st.columns((2, 1))


if st.button('Accept Current State'):
    
    # game.update(1)
    game.current_state = np.array(ag['data'], dtype=int)
    fig, ax = plt.subplots()
    ax.imshow(game.current_state, cmap=cmap)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    f3.pyplot(fig, clear_figure=False)

f1, f2, f3 = st.columns((3, 2, 3))

f3.header("Current State")
f1.header("Previous State")
f2.header("Controls")



with c1:
    container = st.container(border=True)
    # c11, c12 = container.columns((2, 3))
    # Set up the reset button
    # Set up the grid size slider
    # row_size = c11.slider('Row Size', 10, 100, 10)
    # column_size = c11.slider('Column Size', 10, 100, 10)
    # prob = c11.slider('Probability of 1s', 0.0, 1.0, 0.5)
    row_size = container.slider('Row Size', 10, 100, 10)
    column_size = container.slider('Column Size', 10, 100, 10)
    prob = container.slider('Probability of 1s', 0.0, 1.0, 0.5)
    container.write('Create initial state that can be edited by clicking grid')
    if container.button('Initialize zeros'):
        game = GameOfLife(rows=row_size, columns=column_size, prob=prob, randomize=False)
        st.session_state.game = game

        with c2: 
            if "ag" in st.session_state:
                ag = st.session_state.ag
                df = ag['data']
                # game.current_state = np.array(ag['data'], dtype=int)
            else:
                # c12.write(game.current_state)
                df = pd.DataFrame.from_records(np.array(game.current_state, dtype=bool))
                df.columns = [str(a) for a in df.columns]
            
            # gb = GridOptionsBuilder.from_dataframe(df)
            # for col in df.columns:
            #     gb.configure_column(col, editable=True, cellRenderer=checkbox_renderer)
            
            # # st.write('#### interface')
            # ag = AgGrid(
            #     df, 
            #     gridOptions=gb.build(),
            #     fit_columns_on_grid_load=True,
            #     update_mode=GridUpdateMode.MANUAL,
            #     allow_unsafe_jscode=True,
            #     enable_enterprise_modules=False,
            #     theme='alpine',
            # )
            # st.session_state.ag = ag

    if container.button('Initialize random'):
        game = GameOfLife(rows=row_size, columns=column_size, prob=prob)
        st.session_state.game = game

        with c2:
            if "ag" in st.session_state:
                ag = st.session_state.ag
                df = ag['data']
                # game.current_state = np.array(ag['data'], dtype=int)
            else:
                # c12.write(game.current_state)
                df = pd.DataFrame.from_records(np.array(game.current_state, dtype=bool))
                df.columns = [str(a) for a in df.columns]
            
            # gb = GridOptionsBuilder.from_dataframe(df)
            # for col in df.columns:
            #     gb.configure_column(col, editable=True, cellRenderer=checkbox_renderer)

            # # st.write('#### interface')
            # ag = AgGrid(
            #     df, 
            #     gridOptions=gb.build(),
            #     fit_columns_on_grid_load=True,
            #     update_mode=GridUpdateMode.MANUAL,
            #     allow_unsafe_jscode=True,
            #     enable_enterprise_modules=False,
            #     theme='alpine',
            # )
            # st.session_state.ag = ag
            # fig, ax = plt.subplots()
            # ax.imshow(game.current_state, cmap=cmap)
            # ax.get_xaxis().set_ticks([])
            # ax.get_yaxis().set_ticks([])
            # f3.pyplot(fig, clear_figure=False)

with c2:
    if "ag" in st.session_state:
        ag = st.session_state.ag
        df = ag['data']
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
        theme='alpine',
    )
    st.session_state.ag = ag
    # fig, ax = plt.subplots()
    # ax.imshow(game.current_state, cmap=cmap)
    # ax.get_xaxis().set_ticks([])
    # ax.get_yaxis().set_ticks([])
    # f3.pyplot(fig, clear_figure=False)


# # Set up the next button
if f2.button('Next State'):
    
    fig, ax = plt.subplots()
    ax.imshow(game.current_state, cmap=cmap)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    f1.pyplot(fig, clear_figure=False)

    # game.update(1)
    game.life_epoch()
    fig, ax = plt.subplots()
    ax.imshow(game.current_state, cmap=cmap)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    f3.pyplot(fig, clear_figure=False)
# Set up the grid size slider


# # Set up the reset button
# if st.sidebar.button('Reset'):
#     game.randomize()
#     fig, ax = plt.subplots()
#     ax.imshow(game.current_state, cmap=cmap)
#     ax.axis('off')
#     ani = animation.FuncAnimation(fig, animate, frames=50, interval=50)
#     st.pyplot(ani._fig, clear_figure=False)

# # Set up the next button
# if st.sidebar.button('Next'):
#     game.update(1)
#     fig, ax = plt.subplots()
#     ax.imshow(game.current_state, cmap=cmap)
#     ax.axis('off')
#     ani = animation.FuncAnimation(fig, animate, frames=50, interval=50)
#     st.pyplot(ani._fig, clear_figure=False)

# # Set up the randomize button
# if st.sidebar.button('Randomize'):
#     game.randomize()
#     fig, ax = plt.subplots()
#     ax.imshow(game.current_state, cmap=cmap)
#     ax.axis('off')
#     ani = animation.FuncAnimation(fig, animate, frames=50, interval=50)
#     st.pyplot(ani._fig, clear_figure=False)

# # # Set up the clear button
# if st.sidebar.button('Clear'):
#     game.clear()
#     fig, ax = plt.subplots()
#     ax.imshow(game.current_state, cmap=cmap)
#     ax.axis('off')
#     ani = animation.FuncAnimation(fig, animate, frames=50, interval=50)
#     st.pyplot(ani._fig, clear_figure=False)

# # Set up the speed slider
# speed = st.sidebar.slider('Speed', 1, 100, 50)
# ani = animation.FuncAnimation(fig, animate, frames=50, interval=speed)
# st.pyplot(ani._fig, clear_figure=False)

# Set up the author
st.sidebar.title('Author')
st.sidebar.write('This app was created by [Hafiz Issah]()).')

with f2.container(border=True):
    # st.title('For Animation')
    frames = st.slider('Number of iterations', 10, 100, 10)
    Speed = st.slider('Speed', 1, 100, 50)
    if st.button('Animate'):
        fig, ax = plt.subplots()
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        ani = animation.FuncAnimation(fig, animate, frames=frames, interval=Speed)

        with st.spinner("Preparing animation..."):
            # components.html(ani.to_jshtml(), height=550)
            # ani.save('D:\CSM\Mines_Research\Repositories\exploring_dask\GameOLife.gif', writer=PillowWriter())
            ani.save('Current_GameOLife.gif', writer=PillowWriter())

        file_ = open("Current_GameOLife.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()

        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
            unsafe_allow_html=True,
        )

# Set up the socials
b1, b2, b3 = st.columns(3)
b1.write('Author: Hafiz Issah')
b2.info('**[Email](mailto:aissah@gmail.com)**', icon="✉️")
b3.info('**[GitHub](https://github.com/aissah)**', icon="💻")