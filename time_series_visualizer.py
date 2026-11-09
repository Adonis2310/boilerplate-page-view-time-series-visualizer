import calendar

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Importar datos
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# Limpiar datos: quitar el 2.5% superior e inferior
lower = df['value'].quantile(0.025)
upper = df['value'].quantile(0.975)
df = df[(df['value'] >= lower) & (df['value'] <= upper)]


def draw_line_plot():
    df_line = df.copy()

    fig, ax = plt.subplots(figsize=(32, 10))
    ax.plot(df_line.index, df_line['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    df_bar = df.copy()

    # Promedio mensual de vistas, con años como filas y meses como columnas
    df_bar = df_bar.groupby([df_bar.index.year, df_bar.index.month])['value'].mean().unstack()
    df_bar.columns = [calendar.month_name[m] for m in df_bar.columns]

    fig = df_bar.plot(kind='bar', figsize=(12, 8)).figure
    ax = fig.axes[0]
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months', loc='upper left')

    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Preparar datos para los diagramas de caja
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    fig, axes = plt.subplots(1, 2, figsize=(32, 10))

    # Primer diagrama: tendencia por año
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Segundo diagrama: estacionalidad por mes
    sns.boxplot(x='month', y='value', data=df_box, order=month_order, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    fig.savefig('box_plot.png')
    return fig
