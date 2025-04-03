import os
import requests
import json
import streamlit as st
from typing import Dict, Any, Optional
import logging
import time

# Define the base URL
BASE_URL = os.getenv("server_url", "http://127.0.0.1:8000")
BASE_URL = os.getenv("server_url", "https://bushy-321534268367.europe-west1.run.app")

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Utility function for making API requests with error handling and retry logic
def make_api_request(endpoint: str, payload: Dict[str, Any], retries: int = 1, backoff_factor: float = 0.3) -> Optional[Dict[str, Any]]:
    url = f"{BASE_URL}{endpoint}"
    headers = {'Content-Type': 'application/json'}
    
    for attempt in range(retries):
        try:
            with st.spinner('Processing...'):
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                response.raise_for_status()  # Raise an HTTPError for bad responses
                return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            st.error(f"Error: {e}", icon="🔥")
            time.sleep(backoff_factor * (2 ** attempt))  # Exponential backoff
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}")
            st.error(f"Error decoding JSON response: {e}", icon="🔥")
            return None
    
    st.error("Maximum retry limit reached. Please try again later.", icon="🔥")
    return None

# Cache the API call
@st.cache_data
def get_config_from_server_cached(name: str) -> Optional[Dict[str, Any]]:
    return get_config_from_server(name)

def get_config_from_server(name: str) -> Optional[Dict[str, Any]]:
    endpoint = "/config"
    payload = {"name": name}
    return make_api_request(endpoint, payload)

def get_chat_response(area: str, brand: str, name: str, user_query: str) -> Optional[Dict[str, Any]]:
    endpoint = "/chat"
    payload = {"area": area, "brand": brand, "retriever_type": name, "query_text": user_query}
    return make_api_request(endpoint, payload)

# Cache the API call
@st.cache_data 
def get_report_response_cached(task_name: str, inputs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return get_report_response(task_name, inputs)

def get_report_response(name: str, inputs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    endpoint = "/report"
    payload = {"report_name": name, **inputs}
    return make_api_request(endpoint, payload)

# Cache the API call
@st.cache_data 
def get_graph_response_cached(task_name: str, inputs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return get_graph_response(task_name, inputs)

def get_graph_response(name: str, inputs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    endpoint = "/graph"
    payload = {"graph_name": name, **inputs}
    return make_api_request(endpoint, payload)

# Cache the API call
@st.cache_data 
def get_analytics_response_cached(task_name: str, inputs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return get_analytics_response(task_name, inputs)

def get_analytics_response(name: str, inputs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    endpoint = "/analytics"
    payload = {"analytics_name": name, **inputs}
    return make_api_request(endpoint, payload)

# Cache the API call
@st.cache_data 
def get_task_response_cached(name: str, inputs: Dict[str, Any]) -> Optional[str]:
    return get_task_response(name, inputs)

def get_task_response(name: str, inputs: Dict[str, Any]) -> Optional[str]:
    endpoint = "/task"
    payload = {"task_name": name, **inputs}
    response_data = make_api_request(endpoint, payload)
    return response_data.get("response") if response_data else None