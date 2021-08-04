import pytest
import main
from main import *

# tests the get_data() which brings in the tickets
def test_001():
    url = 'https://zccgupta232.zendesk.com/api/v2/tickets.json'
    assert main.get_data(url) != "" 

# tests the API call for each individual ticket
def test_002():
    req_d = {}
    req_d = show_ticket_by_id("23")
    assert(req_d["Ticket ID"]) == 23
    
# tests the API call to see all tickets are retrieved
def test_003():
    df = pd.DataFrame()
    df = show_all()
    assert(len(df)) == 100
    
