import pandas
import plotly.express as px


import dash
import dash_core_components as dcc
import dash_html_components as html

# Öffnet csv als df
m_va = pandas.read_csv('/home/KulturData/mysite/va_m.csv', sep='\t')

# Datum als datetime transformieren
def prep_date():
    m_va['va_datum']  = pandas.to_datetime(
        m_va['va_datum'],
        format= '%d.%m.%Y, %H:%M',
        errors= 'coerce'
        )
prep_date()

# Zeigt min und max Werte
date_von = min(m_va['va_datum'])
date_bis = max(m_va['va_datum'])


# Plotly Graphen
def pro_tag():
    df = m_va.set_index('va_datum').resample('D').size().to_frame('anzahl')
    fig = px.bar(df, x=df.index, y='anzahl')
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(plot_bgcolor='rgb(255,255,255)')
    return fig


def pro_monat():
    df = m_va.set_index('va_datum').resample('M').size().to_frame('anzahl')
    fig = px.bar(df, x=df.index, y='anzahl')
    fig.update_layout(plot_bgcolor='rgb(255,255,255)')
    return fig


def pro_dow():
    m_va.set_index('va_datum')
    m_va['dayofweek'] = m_va['va_datum'].dt.day_name()
    df_1 = m_va.groupby(['dayofweek']).size().to_frame('anzahl')
    df = df_1.sort_values(by='anzahl', ascending=False)
    fig = px.bar(df, x=df.index, y='anzahl')
    fig.update_layout(plot_bgcolor='rgb(255,255,255)')
    return fig

def pro_ort():
    m_va.set_index('va_datum')
    df_1 = m_va.groupby(['va_ort']).size().to_frame('anzahl')
    df = df_1.sort_values(by='anzahl', ascending=False)
    fig = px.pie(df, names=df.index, values='anzahl')
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    return fig


# Webseite initiieren
app = dash.Dash(__name__, meta_tags=[
    # A description of the app, used by e.g.
    # search engines when displaying search results.
    {
        'name': 'description',
        'content': 'Wann finden in München die meisten Veranstaltungen statt? Wann ist die Konkurrenz am geringsten?'
    },
    # A tag that tells the browser not to scale
    # desktop widths to fit mobile screens.
    # Sets the width of the viewport (browser)
    # to the width of the device, and the zoom level
    # (initial scale) to 1.
    #
    # Necessary for "true" mobile support.
    {
      'name': 'viewport',
      'content': 'width=device-width, initial-scale=1.0'
    }
])

# Webseiten Design
app.title = 'Analyse von Veranstaltungen in München'
app.layout = html.Div(
    className='inhalte',
    children=[

    # Logo
    html.Img(src='/assets/kulturdata_logo_rund.png'),

    # Titel
    html.H1('Analyse der Veranstaltungen in München'),
    html.P(
        'Grafischer Überblick über die Verteilung der kommenden Veranstaltungen in München. Betrachtet wird die Zeitspanne von: '
        + str(date_von)
        + ' bis: '
        + str(date_bis)
        ),
    html.P('Die Daten wurden von der Webseite muenchen.de entnommen (webscrapping) und weiterverarbeitet. '
        + 'Dabei wurden NICHT alle Veranstaltungen gezogen, sondern immer nur der erste Termin von einer möglichen Reihe. '
        + 'So entsteht eine Stichprobe an Veranstaltungen, anhand derer sich Muster erkennen lassen. '
        + 'Die Daten werden täglich aktualisiert. Fragen bitte via Twitter an @KulturData.'
        ),
    html.Div(className='strich',children='–––––––––––––––––––––––––'),

    # Grafik 1
    html.H2('Veranstaltungen pro Monat'),
    html.P('Hier seht ihr die summierten Veranstaltungen pro Monat. '
        + 'Die X-Achse zeigt den Monat an. '
        + 'Der Y-Achse könnt ihr die Anzahl der Veranstaltungen in diesem Monat ablesen. '
        + 'Da nicht alle Konzerte lange Zeit im voraus hochgeladen werden, ändert sich an der Anzahl der Konzerte im Verlauf des Jahres noch einiges. '),
    html.Div([dcc.Graph(figure=pro_monat())]),
    html.Div(className='strich',children='–––––––––––––––––––––––––'),

    # Grafik 2
    html.H2('Veranstaltungen pro Tag'),
    html.P('In dieser interaktiven Grafik könnt ihr den unteren Schieberegler bedienen, '
    + 'um einen Zeitraum auszuwählen und reinzuzoomen. So seht ihr die Anzahl pro Tag. '),
    html.Div([dcc.Graph(figure=pro_tag() )]),
    html.Div(className='strich',children='–––––––––––––––––––––––––'),


    # Grafik 3
    html.H2('Verteilung pro Wochentag'),
    html.P('An welchem Wochentag wird am meisten los sein? '
        + 'Diese Darstellung zeigt die Anzahl an kommenden Veranstaltungen pro Wochentag. '),
    html.Div([dcc.Graph(figure=pro_dow())]),
    html.Div(className='strich',children='–––––––––––––––––––––––––'),

    # Grafik 4
    html.H2('Aufteilung nach Konzertort'),
    html.P('München ist bunt, wie dieses Tortendiagramm deutlich macht. '
    + 'Die Prozentzahl ergibt sich aus: Veranstaltungen an diesem Ort / Anzahl aller Veranstaltungen. '
    + 'Wenn man mit der Maus über die einzelne Torte hovert, wird der ausgewählte Konzertort angezeigt. '
    + 'Dadurch muss man die vielen Farbe der Legende nicht unbedingt zuordnen.'),
    html.Div(className='hinweis_torte',children='Du schaust dir diese Webseite von einem Smartphone aus an? '
    + 'Dann wird dir die Grafik leider nicht korrekt angezeigt. Der Bildschirm ist einfach zu klein. Sorry!'),
    html.Div([dcc.Graph(figure=pro_ort())]),


    # Footer
    html.Footer(children=[
        html.A('Hilf mir diese Webseite zu verbessern, indem du diese 3-minütige Umfrage ausfüllst', href='https://us15.list-manage.com/survey?u=35a9651df23316113c0d5d6dd&id=3ea50d28d4'),
        html.Div('-------------------------------'),
        html.Div('© Holger Kurtz | KulturData.de'),
        html.Div('Amalienstraße 57, 80799 München'),
        html.Div('-------------------------------'),
        html.Div('Impressum und Datenschutz finden Sie unter:'),
        html.A('kulturdata.de/impressum', href='https://kulturdata.de/impressum')
        ])

    ])

if __name__ == "__main__":
    app.run_server(debug=True)