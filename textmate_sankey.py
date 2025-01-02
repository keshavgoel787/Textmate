"""
Filename: textmate_sankey.py
Author: Joshua Longo, Keshav Goel
Course: DS3500
Date: Nov 22 2024
Description: The sankey library used to create the sankey diagram for nlp analysis.
"""

# Import statements
import pandas as pd
import plotly.graph_objects as go

# To avoid future warning
pd.set_option('future.no_silent_downcasting', True)

def _code_mapping(df, src, targ):
    """ Map labels in src and targ columns to integers.

    Args:
        df (dataframe): Dataframe
        src (str): Source node column
        targ (str): Target node column

    Returns:
        df, labels (tup): The mapped df and the labels
    """
    # Get the distinct labels
    labels = sorted(list(set(list(df[src]) + list(df[targ]))))

    # Create a label->code mapping
    codes = list(range(len(labels)))
    lc_map = dict(zip(labels, codes))

    # Substitute codes for labels in the dataframe
    df = df.replace({src: lc_map, targ: lc_map})
    return df, labels

def stack(df, src, targ, cols, vals=None):
    """
    This function stacks pairs of columns on to each other to create and transforms a
    dataframe into a standard 2 label dataframe with a values column too.

    Parameters:
        df (dataframe): Dataframe
        src (str): Source node column
        targ (str): Target node column
        cols (tup): Other columns if a multi-layered sankey diagram is desired
        vals (str, optional): Link values (thickness)

    Returns:
        stacked_df (dataframe): the stacked dataframe
    """
    # Empty df for the stacked dataframe
    stacked_df = pd.DataFrame()
    # Concatenate tuples with extra columns in the middle to specify source and target
    total_cols = (src, targ) + cols
    # If else statement for if vals is not provided, so that the occurences can be counted correctly
    if vals:
        # Loop through the source and target pairs
        for sc, tg in zip(total_cols, total_cols[1:]):
            new_df = df[[sc, tg, vals]].groupby([sc, tg]).sum(vals).reset_index()
            new_df.columns = ['src', 'targ', 'count']
            stacked_df = pd.concat([stacked_df, new_df], axis=0, ignore_index=True)
    else:
        for sc, tg in zip(total_cols, total_cols[1:]):
            new_df = df[[sc, tg]].groupby([sc, tg]).size().reset_index(name='count')
            new_df.columns = ['src', 'targ', 'count']
            stacked_df = pd.concat([stacked_df, new_df], axis=0, ignore_index=True)
    # stacked_df.columns = [src, targ, vals]
    return stacked_df

# To make this more modular
def make_sankey(df, src, targ, *cols, vals=None, **kwargs):
    """
    Create a sankey figure.

    Parameters:
        df (dataframe): Dataframe
        src (str): Source node column
        targ (str): Target node column
        *cols (tup): Other columns if a multi-layered sankey diagram is desired
        vals (str, optional): Link values (thickness)
        **kwargs: Other additional keyword arguments for customization

    Returns:
        fig (plotly graph): The sankey diagram
    """
    # Check if there are columns for multi-layer sankey diagrams
    if cols:
        df = stack(df, src, targ, cols, vals=vals)
        values = df['count']
        df, labels = _code_mapping(df, 'src', 'targ')
        link = {'source': df['src'], 'target': df['targ'], 'value': values}
    else:
        if vals:
            values = df[vals]
        else:
            values = [1] * len(df)
        df, labels = _code_mapping(df, src, targ)
        link = {'source': df[src], 'target': df[targ], 'value': values}

    # Set the default thickness and pad for the sankey diagram
    thickness = kwargs.get("thickness", 50)
    pad = kwargs.get("pad", 50)
    line_color = kwargs.get('line_color', 'black')
    line_width = kwargs.get('line_width', 1)

    # Configure node properties such as labels, thickness, padding, and line style
    node = {'label': labels, 'thickness': thickness, 'pad': pad, 'line': {'color': line_color, 'width': line_width}}

    # Create the Sankey diagram object using the configured nodes and links
    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)

    # Update the layout by adding a title and autosizing
    fig.update_layout(
        title=kwargs.get("title", "Sankey Diagram"),
        autosize=True)
    return fig