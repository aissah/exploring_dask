# Build streamlit app for game of life
import base64
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors
from game_of_life_module import GameOfLife
from matplotlib.animation import PillowWriter
import pandas as pd
import streamlit.components.v1 as components
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode

# Set up the game of life
game = GameOfLife()
game.randomize()

# Set up the plot
fig, ax = plt.subplots()
# cmap = colors.ListedColormap(['black', 'white'])
cmap = colors.ListedColormap(['white','black'])
ax.imshow(game.current_state, cmap=cmap)
ax.axis('off')

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
    game.update(i)
    ax.imshow(game.current_state, cmap=cmap, animated=True)
    ax.axis('off')

# fig = plt.figure(figsize=(6, 6))

ani = animation.FuncAnimation(fig, animate, frames=100, interval=100)

# with st.spinner("Preparing animation..."):
#     # components.html(ani.to_jshtml(), height=550)
#     ani.save('D:\CSM\Mines_Research\Repositories\exploring_dask\GameOLife.gif', writer=PillowWriter())

data = {
    'Name': ['a', 'b', 'c'],
    'Paid': [True, False, True],
    'Attended': [False, True, True]
}
# df = pd.DataFrame(data)

df = pd.DataFrame.from_records(np.array(game.current_state, dtype=bool))
df.columns = [str(a) for a in df.columns]

st.write('#### init data')
st.dataframe(df)

gb = GridOptionsBuilder.from_dataframe(df)
for col in df.columns:
    gb.configure_column(col, editable=True, cellRenderer=checkbox_renderer)


st.write('#### interface')
ag = AgGrid(
    df, 
    gridOptions=gb.build(),
    fit_columns_on_grid_load=True,
    allow_unsafe_jscode=True,
    enable_enterprise_modules=False
)

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
row_size = st.sidebar.slider('Row Size', 10, 100, 10)
column_size = st.sidebar.slider('Column Size', 10, 100, 10)
prob = st.sidebar.slider('Probability of 1s', 0.0, 1.0, 0.5)

current_state = np.random.choice([0, 1], (row_size, column_size), p=[1-prob, prob])
fig, ax = plt.subplots()
cmap = colors.ListedColormap(['black', 'white'])
ax.imshow(current_state, cmap=cmap)
ax.axis('off')
# ani = animation.FuncAnimation(fig, animate, frames=100, interval=50)
# st.pyplot(ani._fig, clear_figure=False)


# current_state = np.random.choice([0, 1], (row_size, column_size), p=[1-prob, prob])
st.write(game.current_state)


# Set up the grid size slider
grid_size = st.sidebar.slider('Grid Size', 10, 100, game.current_state.shape[0])
if grid_size != game.current_state.shape[0]:
    game = GameOfLife(grid_size, grid_size)
    game.randomize()
    fig, ax = plt.subplots()
    ax.imshow(game.current_state, cmap=cmap)
    ax.axis('off')
    ani = animation.FuncAnimation(fig, animate, frames=50, interval=50)
    st.pyplot(ani._fig, clear_figure=False)

# # Set up the reset button
if st.sidebar.button('Reset'):
    game.randomize()
    fig, ax = plt.subplots()
    ax.imshow(game.current_state, cmap=cmap)
    ax.axis('off')
    ani = animation.FuncAnimation(fig, animate, frames=50, interval=50)
    st.pyplot(ani._fig, clear_figure=False)

# # Set up the next button
if st.sidebar.button('Next'):
    game.update(1)
    fig, ax = plt.subplots()
    ax.imshow(game.current_state, cmap=cmap)
    ax.axis('off')
    ani = animation.FuncAnimation(fig, animate, frames=50, interval=50)
    st.pyplot(ani._fig, clear_figure=False)

# # Set up the randomize button
if st.sidebar.button('Randomize'):
    game.randomize()
    fig, ax = plt.subplots()
    ax.imshow(game.current_state, cmap=cmap)
    ax.axis('off')
    ani = animation.FuncAnimation(fig, animate, frames=50, interval=50)
    st.pyplot(ani._fig, clear_figure=False)

# # Set up the clear button
if st.sidebar.button('Clear'):
    game.clear()
    fig, ax = plt.subplots()
    ax.imshow(game.current_state, cmap=cmap)
    ax.axis('off')
    ani = animation.FuncAnimation(fig, animate, frames=50, interval=50)
    st.pyplot(ani._fig, clear_figure=False)

# # Set up the speed slider
speed = st.sidebar.slider('Speed', 1, 100, 50)
ani = animation.FuncAnimation(fig, animate, frames=50, interval=speed)
st.pyplot(ani._fig, clear_figure=False)

# Set up the author
st.sidebar.title('Author')
st.sidebar.write('This app was created by [Hafiz Issah]()).')