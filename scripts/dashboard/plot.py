import plotly.express as px

def construct_bar_chart(df, x, y, barmode, title):
    return px.bar(df, x=x, y=y, barmode=barmode, title=title)


def construct_line_chart(df, x, y, title):
    return px.line(df, x=x, y=y, title=title)


def construct_scatter_chart(df, x, y, title):
    return px.scatter(df, x=x, y=y, title=title)

def construct_histogram(df, x, title):
    return px.histogram(df, x=x, title=title)


