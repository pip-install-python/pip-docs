from dash import *
from dash_credit_cards import DashCreditCards, DashParallaxTilt, DashCreditCardInput
import dash_mantine_components as dmc
import json

component = html.Div([
    DashParallaxTilt(
        id='input',
        children=[
            DashCreditCards(
                id='credit_card',
                name='',
                number='',
                expiry='',
                cvc='',
                focused='',
                preview=True,
                issuer='visa',
                locale={"valid": "VALID THRU"},
            )
        ],
        tiltReverse=True,
        glareEnable=True,
        glareMaxOpacity=0.8,
        glareColor='#ffffff',
        glareBorderRadius='20px',
        glarePosition='bottom',
        glareReverse=True,
    ),
    dmc.Space(h=10),
    dmc.Grid([
        dmc.GridCol(span=2),
        dmc.GridCol(dmc.TextInput(
            id='first_name_form',
            # label="First Name",
            # style={"width": 200},
            placeholder="Your First Name",
        ), span=4),
        dmc.GridCol(dmc.TextInput(
            id='last_name_form',
            # label="Last Name",
            # style={"width": 200},
            placeholder="Your Last Name",
        ), span=4),
        dmc.GridCol(span=2)
    ]),
    dmc.Space(h=10),
    html.Center(
        DashCreditCardInput(
            id='credit_card_input',
            cardNumber='',
            cvc='',
            expiry='',
            cardNumberInputProps={'value': ''},
            cardExpiryInputProps={'value': ''},
            cardCVCInputProps={'value': ''},
            fieldClassName="input",
        )
    ),
    dmc.Space(h=10),
    dmc.Grid([
        dmc.Button("Clear", color="red", id="clear"),
        dmc.Space(w=10),
        dmc.Button("Submit", color="green", id="submit")
    ], justify="center"),
    dmc.Space(h=10),
    html.Center(
    dmc.JsonInput(
        id='json_output',
        label="Your json data",
        placeholder="This component will auto-size to fit the content.",
        validationError="Invalid json",
        formatOnBlur=True,
        autosize=True,
        minRows=4,
        style={"width": "20vw"}
    ))

], style={'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center', 'height': '60vh'})


@callback(
    Output('credit_card', 'name', allow_duplicate=True),
    Output('credit_card', 'number', allow_duplicate=True),
    Output('credit_card', 'expiry', allow_duplicate=True),
    Output('credit_card', 'cvc', allow_duplicate=True),
    Output('credit_card', 'issuer', allow_duplicate=True),
    Output('credit_card', 'focused', allow_duplicate=True),
    Input('first_name_form', 'value'),
    Input('last_name_form', 'value'),
    Input('credit_card_input', 'cardNumber'),
    Input('credit_card_input', 'expiry'),
    Input('credit_card_input', 'cvc'),
    prevent_initial_call=True,
)
def update_credit_card(first_name, last_name, card_input, expiry, cvc):
    if not any([card_input, expiry, cvc, first_name, last_name]):
        return no_update
    # Remove spaces and slash from expiry
    expiry = expiry.replace(" ", "").replace("/", "")

    first_digit = card_input[0] if card_input else ''
    if first_digit == '2' or first_digit == '5':
        issuer = 'mastercard'
    elif first_digit == '4':
        issuer = 'visa'
    elif first_digit == '3':
        issuer = 'amex'
    elif first_digit == '6':
        issuer = 'discover'
    else:
        issuer = ''

    # print(expiry, cvc)
    ctx = callback_context
    triggered_component = ctx.triggered[0]["prop_id"].split(".")[0]

    input_focus = None
    if triggered_component == 'credit_card_input':
        input_field = ctx.triggered[0]["prop_id"].split(".")[1]
        if input_field == 'cvc':
            input_focus = "cvc"
        else:
            input_focus = "name"

    name = f"{first_name} {last_name}"
    return name, card_input, expiry, cvc, issuer, input_focus


@callback(
    Output('json_output', 'value'),
    Output('first_name_form', 'value'),
    Output('last_name_form', 'value'),
    Output('credit_card_input', 'cardNumber'),
    Output('credit_card_input', 'expiry'),
    Output('credit_card_input', 'cvc'),
    Output('credit_card', 'name'),
    Output('credit_card', 'number'),
    Output('credit_card', 'expiry'),
    Output('credit_card', 'cvc'),
    Output('credit_card', 'focused'),
    Output('credit_card', 'issuer'),
    Input('submit', 'n_clicks'),
    Input('clear', 'n_clicks'),
    State('first_name_form', 'value'),
    State('last_name_form', 'value'),
    State('credit_card_input', 'cardNumber'),
    State('credit_card_input', 'expiry'),
    State('credit_card_input', 'cvc'),
    prevent_initial_call=True,
)
def update_output(submit_n_clicks, clear_n_clicks, first_name, last_name, card_number, expiry, cvc):
    ctx = callback_context
    if not ctx.triggered:
        return no_update
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'submit':
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'card_number': card_number,
            'expiry': expiry,
            'cvc': cvc,
        }
        return (json.dumps(data, indent=2), no_update, no_update, no_update, no_update, no_update, no_update, no_update,
                no_update, no_update, no_update, no_update)
    elif button_id == 'clear':
        return '', '', '', '', '', '', '', '', '', '', '', ''
