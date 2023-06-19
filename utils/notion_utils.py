import requests
from .env_utils import notion_token, notion_db_id

headers = {
    "Notion-Version": "2021-08-16",
    "Authorization": f"Bearer {notion_token}",
    "Content-Type": "application/json"
}

def get_rows(start, end):
    response = requests.post(
        f"https://api.notion.com/v1/databases/{notion_db_id}/query",
        json={
                "filter": {
                "and":[
                        {
                            "property": "状态",
                            "select": {
                                "is_empty": True
                            }
                        },
                        {
                            "property": "起止日期",
                            "date": {
                                "before": end
                            }
                        },
                                            {
                            "property": "起止日期",
                            "date": {
                                "after": start
                            }
                        }
                    ]
                },
                "sorts": [
                    {
                        "property": "起止日期",
                        "direction": "ascending"
                    }
                ]
            },
        headers=headers
    )
    return response.json()

