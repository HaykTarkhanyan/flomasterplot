import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def one_numeric(df, col_name, plot_type="Histogram"):
    """
        ['Histogram', 'Distplot']
    """
    if plot_type=='Histogram':
        fig = px.histogram(df, x=col_name) 
        fig.update_layout(bargap=0.2)
    if plot_type=='Distplot':
        fig = ff.create_distplot([df[col_name]], group_labels=['distplot'])
    return fig

def two_numeric(df, x, y, plot_type='Scatter'):
    """
        ["Scatter", "Scatter plot with margins", "2D density plot", "Distplot", "Histogram"]
        ["Line plot", 'Connected Scatter', "Area plot"]

    """
    x1 = df[x]
    x2 = df[y]


    if plot_type=='Scatter':
        fig = px.scatter(df, x, y)
    
    if plot_type=='Scatter plot with margins':
        fig = px.scatter(df, x, y, marginal_x="histogram", marginal_y="histogram")

    if plot_type=='2D density plot':
        colorscale = ['#7A4579', '#D56073', 'rgb(236,158,105)', (1, 1, 0.2), (0.98,0.98,0.98)]

        fig = ff.create_2d_density(df[x].to_list(), df[y].to_list(), colorscale=colorscale,
                                hist_color='rgb(255, 237, 222)', point_size=3)
    
    if plot_type=='Distplot':
        group_labels = [x,y]
        colors = ['slategray', 'magenta']
        fig = ff.create_distplot([x1, x2], group_labels, bin_size=.5,
                                curve_type='normal',colors=colors)
        fig.update_layout(title_text='Distplot with Normal Distribution')

    if plot_type=='Histogram':
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=x1))
        fig.update_layout(bargap=0.2)
        fig.add_trace(go.Histogram(x=x2))
        fig.update_layout(barmode='overlay')
        fig.update_traces(opacity=0.75)
        fig.update_layout(bargap=0.2)
    
    if plot_type=='Line plot':
        fig = px.line(df, x, y)

    if plot_type=='Connected Scatter':
        fig = px.line(df, x, y, markers=True)

    if plot_type=="Area plot":
        fig = px.area(df, x ,y)

    return fig

def one_categoric(df, col_name, plot_type='Histogram'):
    """
        plot type one of ['Donut', 'Pie', 'Histogram']
    """

    feat = list(df[col_name])
    if plot_type=='Donut':
        fig = go.Figure(data=[go.Pie(labels=feat, hole=.4)]) 
    
    if plot_type=='Pie':
        fig = go.Figure(data=[go.Pie(labels=feat)]) 

    if plot_type=='Histogram':
        fig = px.histogram(df, x=col_name, color=col_name)
        fig.update_layout(bargap=0.2)

    return fig

def one_textual(df, col_name):
    text = " ".join(df[col_name].dropna().to_list())
    print(text)
    wordcloud = WordCloud(width=480, height=480, margin=0).generate(text)
    # print(wordcloud)
    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    # plt.margins(x=0, y=0)
    # plt.show()
    # return plt
    # return fig

def numeric_categorical(df, x, y, plot_type="Box"):
    """
        ["Violin", "Box"]
    """
