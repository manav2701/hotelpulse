from src.agents.marketing_agent import generate_marketing_alert

def test_agent_no_trigger():
    result = generate_marketing_alert(0.80, "Jan 1", "City Hotel", threshold=0.65)
    assert result['triggered'] == False
    assert result['message'] is None
