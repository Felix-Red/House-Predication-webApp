from urllib.parse import quote

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import joblib
import pandas as pd


# Load the model
model = joblib.load('forest_model.plk')

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = 'King County Home Value Estimator'
server = app.server

# Define dropdown options
max_bedrooms = 6
max_bathrooms = 6
max_floors = 3
index = [0]
view_options = list(range(5))
condition_options = list(range(1, 6))
grade_options = list(range(1, 14))


def svg_data_uri(svg):
    """Return a compact SVG data URI for the small interface icons."""
    return 'data:image/svg+xml,' + quote(svg)


home_icon = svg_data_uri(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" fill="none" '
    'stroke="#10552b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M7 22 24 7l17 15"/><path d="M12 20v21h24V20"/>'
    '<path d="M20 41V29h8v12"/></svg>'
)
location_icon = svg_data_uri(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" fill="none" '
    'stroke="#10552b" stroke-width="2.7" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M38 20c0 10-14 24-14 24S10 30 10 20a14 14 0 1 1 28 0Z"/>'
    '<circle cx="24" cy="20" r="5"/></svg>'
)
brand_icon = svg_data_uri(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 64" fill="none" '
    'stroke="#10552b" stroke-width="6" stroke-linecap="square" stroke-linejoin="miter">'
    '<path d="M8 38 48 5l40 33"/><path d="M71 24V8h9v24"/>'
    '<path d="M31 48h11v11H31zM48 48h11v11H48zM31 31h11v11H31zM48 31h11v11H48z" '
    'fill="#10552b" stroke-width="1"/></svg>'
)
user_icon = svg_data_uri(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" fill="none" '
    'stroke="#10552b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="16" cy="10" r="5"/><path d="M5.5 27c.5-5.6 4.6-9 10.5-9s10 3.4 10.5 9"/></svg>'
)


def field(label, component, control_id=None):
    label_target = control_id or getattr(component, 'id', None)
    return html.Div(
        [
            html.Label(label, htmlFor=label_target, className='field-label'),
            component,
        ],
        className='form-field',
    )


def dropdown(component_id, options, value=None, placeholder=None):
    return dcc.Dropdown(
        id=component_id,
        options=options,
        value=value,
        placeholder=placeholder,
        clearable=False,
        searchable=False,
        className='estimator-dropdown',
    )


def number_input(component_id, value=None, placeholder=None):
    return dcc.Input(
        id=component_id,
        type='number',
        value=value,
        placeholder=placeholder,
        className='estimator-input',
        min=0,
        step=1,
    )


def section_heading(icon, title, location=False):
    return html.Div(
        [
            html.Div(html.Img(src=icon, alt=''), className='section-icon'),
            html.H2(title, className='section-title'),
            html.Div(className='section-rule'),
        ],
        className='section-heading' + (' section-heading-location' if location else ''),
    )


# Define the layout of the app
app.layout = html.Div(
    className='app-shell',
    children=[
        html.Header(
            className='site-header',
            children=html.Div(
                className='header-inner',
                children=[
                    html.Img(src=brand_icon, alt='', className='brand-mark'),
                    html.Div(className='header-divider'),
                    html.Div('King County', className='brand-name'),
                    html.Div(className='header-divider header-divider-secondary'),
                    html.Div('Home value estimator', className='product-name'),
                    html.Div(
                        html.Img(src=user_icon, alt='Account', className='account-icon'),
                        className='account-avatar',
                        title='Account',
                    ),
                ],
            ),
        ),
        html.Main(
            className='page-content',
            children=[
                html.Section(
                    className='hero',
                    children=[
                        html.Div(
                            [
                                html.Span(className='eyebrow-rule'),
                                html.Span('Property estimate'),
                                html.Span(className='eyebrow-rule'),
                            ],
                            className='eyebrow',
                        ),
                        html.H1('Estimate your home’s value', className='hero-title'),
                        html.P(
                            'Enter property details to generate an estimated market value.',
                            className='hero-description',
                        ),
                    ],
                ),
                html.Section(
                    className='estimator-card',
                    children=[
                        section_heading(home_icon, 'Property details'),
                        html.Div(
                            className='property-grid',
                            children=[
                                field(
                                    'Number of Bedrooms',
                                    dropdown(
                                        'bedrooms-dropdown',
                                        [{'label': str(i), 'value': i} for i in range(1, max_bedrooms + 1)],
                                        value=3,
                                    ),
                                ),
                                field(
                                    'Number of Bathrooms',
                                    dropdown(
                                        'bathrooms-dropdown',
                                        [{'label': str(i), 'value': i} for i in range(1, max_bathrooms + 1)],
                                        value=2,
                                    ),
                                ),
                                field(
                                    'Square Foot of Interior',
                                    html.Div(
                                        [number_input('sqft-interior-input', value=1500), html.Span('sq ft')],
                                        className='input-with-unit',
                                    ),
                                    control_id='sqft-interior-input',
                                ),
                                field(
                                    'Square Foot of Land',
                                    html.Div(
                                        [number_input('sqft-land-input', value=5000), html.Span('sq ft')],
                                        className='input-with-unit',
                                    ),
                                    control_id='sqft-land-input',
                                ),
                                field(
                                    'Number of Floors',
                                    dropdown(
                                        'floors-dropdown',
                                        [{'label': str(i), 'value': i} for i in range(1, max_floors + 1)],
                                        value=1,
                                    ),
                                ),
                                field(
                                    'Overlooking Waterfront',
                                    dropdown(
                                        'waterfront-dropdown',
                                        [
                                            {'label': 'Yes', 'value': 1},
                                            {'label': 'No', 'value': 0},
                                        ],
                                        placeholder='Select...',
                                    ),
                                ),
                                field(
                                    'View',
                                    dropdown(
                                        'view-dropdown',
                                        [{'label': str(option), 'value': option} for option in view_options],
                                        value=0,
                                    ),
                                ),
                                field(
                                    'Condition (1–5)',
                                    dropdown(
                                        'condition-dropdown',
                                        [{'label': str(option), 'value': option} for option in condition_options],
                                        value=3,
                                    ),
                                ),
                                field(
                                    'Grade (1–13)',
                                    dropdown(
                                        'grade-dropdown',
                                        [{'label': str(option), 'value': option} for option in grade_options],
                                        value=7,
                                    ),
                                ),
                            ],
                        ),
                        html.Section(
                            className='location-panel',
                            children=[
                                section_heading(location_icon, 'Location', location=True),
                                html.Div(
                                    className='location-grid',
                                    children=[
                                        field('Latitude', number_input('latitude', placeholder='')),
                                        field('Longitude', number_input('Longitude', placeholder='')),
                                    ],
                                ),
                            ],
                        ),
                        html.Button(
                            [html.Span('Estimate home value'), html.Span('→', className='button-arrow')],
                            id='submit-val',
                            n_clicks=0,
                            className='estimate-button',
                        ),
                        html.Div(id='output-prediction', className='prediction-output', role='status'),
                    ],
                ),
            ],
        ),
    ],
)


# Define callback to make predictions when the button is clicked
@app.callback(
    Output('output-prediction', 'children'),
    [Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('bedrooms-dropdown', 'value'),
     dash.dependencies.State('bathrooms-dropdown', 'value'),
     dash.dependencies.State('sqft-interior-input', 'value'),
     dash.dependencies.State('sqft-land-input', 'value'),
     dash.dependencies.State('floors-dropdown', 'value'),
     dash.dependencies.State('waterfront-dropdown', 'value'),
     dash.dependencies.State('view-dropdown', 'value'),
     dash.dependencies.State('condition-dropdown', 'value'),
     dash.dependencies.State('grade-dropdown', 'value'),
     dash.dependencies.State('latitude', 'value'),
     dash.dependencies.State('Longitude', 'value')]
)
def update_prediction(n_clicks, bedrooms, bathrooms, sqft_living, sqft_lot, floors, waterfront, view, condition, grade, lat, long):
    if not n_clicks:
        return ''

    required_values = [
        bedrooms,
        bathrooms,
        sqft_living,
        sqft_lot,
        floors,
        waterfront,
        view,
        condition,
        grade,
        lat,
        long,
    ]
    if any(value is None for value in required_values):
        return html.Div(
            'Please complete all property details, including waterfront status and location.',
            className='prediction-message',
        )

    # Combine bathrooms and bedrooms
    number_of_rooms = bathrooms + bedrooms

    # Prepare the input data for prediction
    data = pd.DataFrame(
        {
            'bedrooms': [bedrooms],
            'bathrooms': [bathrooms],
            'sqft_living': [sqft_living],
            'sqft_lot': [sqft_lot],
            'floors': [floors],
            'waterfront': [waterfront],
            'view': [view],
            'condition': [condition],
            'grade': [grade],
            'lat': [lat],
            'long': [long],
            'NumberofRooms': [number_of_rooms],
        },
        index,
    )

    # Make prediction using the model
    prediction = model.predict(data)[0]
    return html.Div(
        [
            html.Span('Estimated market value', className='prediction-label'),
            html.Strong(f'${prediction:,.2f}', className='prediction-value'),
        ],
        className='prediction-card',
    )


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
