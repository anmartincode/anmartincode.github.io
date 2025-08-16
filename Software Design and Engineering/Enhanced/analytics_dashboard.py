#!/usr/bin/env python3
"""
Enhanced Analytics Dashboard for Animal Shelter Management System
Interactive dashboard with real-time data visualization and ML insights
"""

import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import json
import time
from typing import Dict, List, Any

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Enhanced Animal Shelter Analytics Dashboard"

# Configuration
API_BASE_URL = "http://localhost:5000/api"
REFRESH_INTERVAL = 30000  # 30 seconds

# Layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("🐾 Enhanced Animal Shelter Analytics Dashboard", 
                   className="text-center text-primary mb-4"),
            html.Hr()
        ])
    ]),
    
    # Authentication Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Authentication"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Input(id="username-input", placeholder="Username", type="text"),
                        ], width=6),
                        dbc.Col([
                            dbc.Input(id="password-input", placeholder="Password", type="password"),
                        ], width=6),
                    ]),
                    dbc.Button("Login", id="login-button", color="primary", className="mt-2"),
                    html.Div(id="auth-status", className="mt-2")
                ])
            ])
        ])
    ], className="mb-4"),
    
    # Key Metrics Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="total-animals", className="card-title"),
                    html.P("Total Animals", className="card-text")
                ])
            ], color="info", outline=True)
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="adopted-animals", className="card-title"),
                    html.P("Adopted Animals", className="card-text")
                ])
            ], color="success", outline=True)
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="adoption-rate", className="card-title"),
                    html.P("Adoption Rate", className="card-text")
                ])
            ], color="warning", outline=True)
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="recent-adoptions", className="card-title"),
                    html.P("Recent Adoptions (30 days)", className="card-text")
                ])
            ], color="danger", outline=True)
        ], width=3),
    ], className="mb-4"),
    
    # Charts Row 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Animals by Type"),
                dbc.CardBody([
                    dcc.Graph(id="animals-by-type-chart")
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Adoption Trends"),
                dbc.CardBody([
                    dcc.Graph(id="adoption-trends-chart")
                ])
            ])
        ], width=6),
    ], className="mb-4"),
    
    # Charts Row 2
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Behavior Score Distribution"),
                dbc.CardBody([
                    dcc.Graph(id="behavior-score-chart")
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Adoption Probability vs Age"),
                dbc.CardBody([
                    dcc.Graph(id="adoption-probability-chart")
                ])
            ])
        ], width=6),
    ], className="mb-4"),
    
    # ML Predictions Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Machine Learning Predictions"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Input(id="prediction-name", placeholder="Animal Name", type="text"),
                        ], width=3),
                        dbc.Col([
                            dbc.Input(id="prediction-age", placeholder="Age", type="number"),
                        ], width=2),
                        dbc.Col([
                            dcc.Dropdown(
                                id="prediction-type",
                                options=[
                                    {"label": "Dog", "value": "Dog"},
                                    {"label": "Cat", "value": "Cat"},
                                    {"label": "Bird", "value": "Bird"},
                                    {"label": "Other", "value": "Other"}
                                ],
                                placeholder="Animal Type"
                            )
                        ], width=3),
                        dbc.Col([
                            dbc.Input(id="prediction-breed", placeholder="Breed", type="text"),
                        ], width=2),
                        dbc.Col([
                            dbc.Button("Predict", id="predict-button", color="success"),
                        ], width=2),
                    ], className="mb-3"),
                    html.Div(id="prediction-results")
                ])
            ])
        ])
    ], className="mb-4"),
    
    # Recent Adoptions Table
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Recent Adoptions"),
                dbc.CardBody([
                    html.Div(id="recent-adoptions-table")
                ])
            ])
        ])
    ], className="mb-4"),
    
    # Auto-refresh interval
    dcc.Interval(
        id='interval-component',
        interval=REFRESH_INTERVAL,
        n_intervals=0
    ),
    
    # Store for authentication token
    dcc.Store(id='auth-token'),
    
], fluid=True)

# Global variables for authentication
auth_token = None

def make_api_request(endpoint: str, method: str = "GET", data: Dict = None, token: str = None) -> Dict:
    """Make API request with authentication"""
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        if method == "GET":
            response = requests.get(f"{API_BASE_URL}{endpoint}", headers=headers)
        elif method == "POST":
            response = requests.post(f"{API_BASE_URL}{endpoint}", headers=headers, json=data)
        else:
            return {"error": "Unsupported method"}
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection Error: {str(e)}"}

# Callbacks

@app.callback(
    [Output("auth-status", "children"),
     Output("auth-token", "data")],
    [Input("login-button", "n_clicks")],
    [State("username-input", "value"),
     State("password-input", "value")]
)
def handle_login(n_clicks, username, password):
    """Handle user login"""
    if not n_clicks or not username or not password:
        return "Please enter credentials", None
    
    login_data = {"username": username, "password": password}
    response = make_api_request("/auth/login", "POST", login_data)
    
    if "error" in response:
        return f"Login failed: {response['error']}", None
    else:
        token = response.get("access_token")
        return f"Welcome, {username}!", token

@app.callback(
    [Output("total-animals", "children"),
     Output("adopted-animals", "children"),
     Output("adoption-rate", "children"),
     Output("recent-adoptions", "children")],
    [Input("interval-component", "n_intervals"),
     Input("auth-token", "data")]
)
def update_metrics(n_intervals, token):
    """Update key metrics"""
    if not token:
        return "N/A", "N/A", "N/A", "N/A"
    
    response = make_api_request("/analytics/dashboard", token=token)
    
    if "error" in response:
        return "Error", "Error", "Error", "Error"
    
    data = response
    total = data.get("total_animals", 0)
    adopted = data.get("adopted_animals", 0)
    rate = data.get("adoption_rate", 0)
    recent = data.get("recent_adoptions_count", 0)
    
    return f"{total:,}", f"{adopted:,}", f"{rate:.1f}%", f"{recent:,}"

@app.callback(
    Output("animals-by-type-chart", "figure"),
    [Input("interval-component", "n_intervals"),
     Input("auth-token", "data")]
)
def update_animals_by_type_chart(n_intervals, token):
    """Update animals by type chart"""
    if not token:
        return go.Figure()
    
    response = make_api_request("/analytics/dashboard", token=token)
    
    if "error" in response:
        return go.Figure()
    
    data = response.get("animals_by_type", {})
    
    if not data:
        return go.Figure()
    
    fig = px.pie(
        values=list(data.values()),
        names=list(data.keys()),
        title="Animals by Type"
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig

@app.callback(
    Output("adoption-trends-chart", "figure"),
    [Input("interval-component", "n_intervals"),
     Input("auth-token", "data")]
)
def update_adoption_trends_chart(n_intervals, token):
    """Update adoption trends chart"""
    if not token:
        return go.Figure()
    
    # Get trend analysis data
    response = make_api_request("/analytics/reports", "POST", {"type": "trend_analysis"}, token)
    
    if "error" in response:
        return go.Figure()
    
    data = response.get("data", {})
    trends = data.get("monthly_trends", [])
    
    if not trends:
        return go.Figure()
    
    months = [t["month"] for t in trends]
    adoptions = [t["adoptions"] for t in trends]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months,
        y=adoptions,
        mode='lines+markers',
        name='Adoptions',
        line=dict(color='blue', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Monthly Adoption Trends",
        xaxis_title="Month",
        yaxis_title="Number of Adoptions",
        showlegend=False
    )
    
    return fig

@app.callback(
    Output("behavior-score-chart", "figure"),
    [Input("interval-component", "n_intervals"),
     Input("auth-token", "data")]
)
def update_behavior_score_chart(n_intervals, token):
    """Update behavior score distribution chart"""
    if not token:
        return go.Figure()
    
    # Get animals data
    response = make_api_request("/animals", token=token)
    
    if "error" in response:
        return go.Figure()
    
    animals = response.get("animals", [])
    
    if not animals:
        return go.Figure()
    
    # Extract behavior scores
    behavior_scores = [a.get("behavior_score", 0) for a in animals if a.get("behavior_score") is not None]
    
    if not behavior_scores:
        return go.Figure()
    
    fig = px.histogram(
        x=behavior_scores,
        nbins=20,
        title="Behavior Score Distribution",
        labels={"x": "Behavior Score", "y": "Count"}
    )
    
    fig.update_layout(
        xaxis_title="Behavior Score",
        yaxis_title="Number of Animals"
    )
    
    return fig

@app.callback(
    Output("adoption-probability-chart", "figure"),
    [Input("interval-component", "n_intervals"),
     Input("auth-token", "data")]
)
def update_adoption_probability_chart(n_intervals, token):
    """Update adoption probability vs age chart"""
    if not token:
        return go.Figure()
    
    # Get animals data
    response = make_api_request("/animals", token=token)
    
    if "error" in response:
        return go.Figure()
    
    animals = response.get("animals", [])
    
    if not animals:
        return go.Figure()
    
    # Extract age and adoption probability
    data_points = []
    for animal in animals:
        age = animal.get("age")
        prob = animal.get("adoption_probability")
        if age is not None and prob is not None:
            data_points.append({"age": age, "probability": prob})
    
    if not data_points:
        return go.Figure()
    
    df = pd.DataFrame(data_points)
    
    fig = px.scatter(
        df,
        x="age",
        y="probability",
        title="Adoption Probability vs Age",
        labels={"age": "Age (years)", "probability": "Adoption Probability"}
    )
    
    # Add trend line
    z = np.polyfit(df["age"], df["probability"], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(
        x=df["age"],
        y=p(df["age"]),
        mode='lines',
        name='Trend Line',
        line=dict(color='red', dash='dash')
    ))
    
    return fig

@app.callback(
    Output("prediction-results", "children"),
    [Input("predict-button", "n_clicks")],
    [State("prediction-name", "value"),
     State("prediction-age", "value"),
     State("prediction-type", "value"),
     State("prediction-breed", "value"),
     State("auth-token", "data")]
)
def make_prediction(n_clicks, name, age, animal_type, breed, token):
    """Make ML prediction for animal data"""
    if not n_clicks or not token:
        return ""
    
    if not all([name, age, animal_type, breed]):
        return dbc.Alert("Please fill in all fields", color="warning")
    
    prediction_data = {
        "name": name,
        "age": age,
        "animal_type": animal_type,
        "breed": breed,
        "health_score": 0.7  # Default value
    }
    
    response = make_api_request("/analytics/predictions", "POST", prediction_data, token)
    
    if "error" in response:
        return dbc.Alert(f"Prediction failed: {response['error']}", color="danger")
    
    behavior_score = response.get("behavior_score", 0)
    adoption_probability = response.get("adoption_probability", 0)
    recommendations = response.get("recommendations", [])
    
    return dbc.Card([
        dbc.CardHeader("Prediction Results"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H5("Behavior Score"),
                    html.H3(f"{behavior_score:.1%}", className="text-primary")
                ], width=4),
                dbc.Col([
                    html.H5("Adoption Probability"),
                    html.H3(f"{adoption_probability:.1%}", className="text-success")
                ], width=4),
                dbc.Col([
                    html.H5("Recommendations"),
                    html.Ul([html.Li(rec) for rec in recommendations])
                ], width=4),
            ])
        ])
    ])

@app.callback(
    Output("recent-adoptions-table", "children"),
    [Input("interval-component", "n_intervals"),
     Input("auth-token", "data")]
)
def update_recent_adoptions_table(n_intervals, token):
    """Update recent adoptions table"""
    if not token:
        return "Please login to view data"
    
    response = make_api_request("/analytics/dashboard", token=token)
    
    if "error" in response:
        return f"Error loading data: {response['error']}"
    
    recent_adoptions = response.get("recent_adoptions", [])
    
    if not recent_adoptions:
        return "No recent adoptions found"
    
    # Create table
    table_header = [
        html.Thead(html.Tr([
            html.Th("Name"),
            html.Th("Type"),
            html.Th("Breed"),
            html.Th("Age"),
            html.Th("Adoption Date")
        ]))
    ]
    
    table_rows = []
    for adoption in recent_adoptions[:10]:  # Show last 10
        table_rows.append(html.Tr([
            html.Td(adoption.get("name", "N/A")),
            html.Td(adoption.get("animal_type", "N/A")),
            html.Td(adoption.get("breed", "N/A")),
            html.Td(adoption.get("age", "N/A")),
            html.Td(adoption.get("outcome_date", "N/A")[:10] if adoption.get("outcome_date") else "N/A")
        ]))
    
    table_body = [html.Tbody(table_rows)]
    
    return dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True)

# Run the app
if __name__ == '__main__':
    print("Starting Enhanced Analytics Dashboard...")
    print("Make sure the main API server is running on http://localhost:5000")
    app.run_server(debug=True, port=8050, host='0.0.0.0')
