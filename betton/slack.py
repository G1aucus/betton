import requests
from bs4 import BeautifulSoup


def skicka_notis(del1, del2, del3, del4):
    webhook_url = "https://hooks.slack.com/services/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" # Slack webhook
    payload = {
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Match",
				"emoji": True
			}
		},
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": del1,
				"emoji": True
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "ELO:",
				"emoji": True
			}
		},
		{
			"type": "rich_text",
			"elements": [
				{
					"type": "rich_text_section",
					"elements": [
						{
							"type": "text",
							"text": del2,
							"style": {
								"italic": True
							}
						}
					]
				}
			]
		},
        {
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Odds",
				"emoji": True
			}
		},
		{
			"type": "rich_text",
			"elements": [
				{
					"type": "rich_text_section",
					"elements": [
						{
							"type": "text",
							"text": del3,
							"style": {
								"italic": True
							}
						}
					]
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": del4,
				"emoji": True
			}
		}
	]
    }

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print("Notification sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending notification: {e}")
