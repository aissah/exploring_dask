import plotly.express as px
import streamlit as st


def create_blank_grid(size):
    return [[0] * size for _ in range(size)]


def main():
    st.title("Grid Input App")

    # Get grid size from user input
    grid_size = st.slider("Select grid size:", min_value=3, max_value=10, value=5)

    # Create a blank grid
    grid = create_blank_grid(grid_size)

    # Display the grid using Plotly
    fig = px.imshow(
        grid, binary_string=True, labels=dict(color="Click on the cells to toggle")
    )
    fig.update_layout(width=400, height=400)

    # Show the Plotly figure
    st.plotly_chart(fig, use_container_width=True)

    # Handle grid clicks
    clicked_cells = st.button("Submit Clicks")

    if clicked_cells:
        # Get the clicked points from the Plotly figure
        clicked_points = st.session_state.mouse_click_data["points"]

        # Update the grid based on clicked points
        for point in clicked_points:
            row, col = int(point["y"]), int(point["x"])
            grid[row][col] = 1 - grid[row][col]  # Toggle the value (0 to 1 or 1 to 0)

        # Display the updated grid
        st.write("Updated Grid:")
        st.write(grid)


if __name__ == "__main__":
    if "mouse_click_data" not in st.session_state:
        st.session_state.mouse_click_data = {"points": []}
    main()
