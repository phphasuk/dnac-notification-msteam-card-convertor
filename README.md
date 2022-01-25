# dnac-notification-msftteam-card-convertor


*DNAC Webhook Adapter for Microsoft Team*

---

**ToDo's:**

- Any comments, Please email to me @ phphasuk@cisco.com

---

## Motivation

DNA Center can use webhook to send the event notifications in real-time. Many messaging platforms support incoming webhook today including Cisco Webex, and Microsoft Team. However, the Microsoft Team incoming webhook connector requires the webhook payload in microsoft card format. The DNA Center webhook event is in different JSON format. This script will accept the DNA Center webhook notification in JSON format, and then convert it into the supported microsoft card format.

## Features

- Receiving DNAC webhook events and record events into a file
- Converting the DNAC webhook events to Microsoft adaptive card amd forward it to Microsoft Team
- Adaptive card content is customized using Jinja2 Template

## Technologies & Frameworks Used

This is Cisco Sample Code using Python Programming

**Cisco Products & Services:**

- DNA Center

## Prerequisite steps

- install required python modules, please refer to requirements.txt
- adding this script as a webhook receiver in DNAC
- adding incomming webhook connector in Microsoft Team Channel


## File Description

File Description:
- "config.py" – Configuration File (DNAC IP / Port Number)
- "dnac-notification-msteam-card-convertor.py" – webhook receiver and format converter script
- "Requirements.txt" – Needed python modules
- "adaptive_card_template.j2" - Microsoft Adaptive card template in Jinja2

## "adaptive_card_template.j2" File

```
{
    "type": "message",
    "attachments": [
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.2",
            "content": {
                "type": "AdaptiveCard",
                "body": [
                    {
                        "type": "TextBlock",
                        "size": "Medium",
                        "weight": "Bolder",
                        "text": "DNA Center Event Notification",
                        "wrap": true
                    },
                    {
                        "type": "FactSet",
                        "wrap": true,
                        "facts": [
                            {
                                "title": "Instance ID",
                                "value": "{{ instanceId }}"
                            },
                            {
                                "title": "Event ID",
                                "value": "{{ eventId }}"
                            },
                            {
                                "title": "Event Name",
                                "value": "{{ name }}"
                            },
                            {
                                "title": "Event Description",
                                "value": "{{ description }}"
                            },
                            {
                                "title": "Time Stamp",
                                "value": "{{ timestamp }}"
                            },
                            {
                                "title": "From DNA Center",
                                "value": "{{ dnacIP }}"
                            }
                        ]
                    },
                    {
                        "type": "TextBlock",
                        "text": "{{ details }}",
                        "wrap": true
                    }
                ],
                "actions": [
                    {
                        "type": "Action.OpenUrl",
                        "title": "View",
                        "url": "{{ ciscoDnaEventLink }}"
                    }
                ]
            }
        }
    ]
}
```
## Installation

- Install the required python module
```
pip install -r requirements.txt
```

- Configure required information in config.py
```
WEBHOOK_HOST = 'THIS WEBHOOK SERVER's IP ADDRESS'
WEBHOOK_PORT = 'THIS WEBHOOK SERVER's PORT'
WEBHOOK_USERNAME = 'THIS WEBHOOK SERVER's username'
WEBHOOK_PASSWORD = 'THIS WEBHOOK SERVER's password'
TEAM_WEBHOOK_URL = 'MICROSOFT TEAM INCOMMING WEBHOOK URL'
```

## Usage

Script usage arguments:
```
$ python dnac-notification-msteam-card-convertor.py

```

## Authors & Maintainers

- Phithakkit Phasuk <phphasuk@cisco.com>

## Credits

- https://developer.cisco.com/

## License

This project is licensed to you under the terms of the [Cisco Sample
Code License](./LICENSE).

