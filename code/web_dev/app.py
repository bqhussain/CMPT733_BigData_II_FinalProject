import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from apps import patient_info, anit
from app_temp import app

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "14rem",
    "padding": "2rem 1rem",
    "background-color": "#D3D3D3",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "14rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

link_ids = ['anti', 'AEP', 'patient_info']
link_label = ['Antibiotic Effectiveness Dashboard', 'Antibiotic Effectiveness Prediction', 'Mortality Rate and LOS Prediction']

navLinks = []
for i in range(len(link_ids)):
    # tab sequence
    link_dir = "http://0.0.0.0:5005"
    if link_ids[i] == 'AEP':
        navLinks.append(dbc.NavLink(f"{link_label[i]}", href=f"{link_dir}", id=f"{link_ids[i]}"))
    else:
        navLinks.append(dbc.NavLink(f"{link_label[i]}", href=f"/{link_ids[i]}", id=f"{link_ids[i]}"))

sidebar = html.Div(
    [
        dbc.Nav(
            navLinks,
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"{link_ids[i]}", "active") for i in range(len(link_ids))],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/{link_ids[i]}" for i in range(len(link_ids))]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    print(pathname)
    if pathname in ["/", "/anti"]:
        return anit.layout
    elif pathname == "/patient_info":
        return patient_info.layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8088, debug=False)