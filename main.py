from markdown import markdown
from utils_data import load_toml, format_template
from utils_email import get_creds, send_email


def main():
    json = load_toml()
    for university in json["recipient"]["universities"]:
        body_text = format_template(json["email"]['body'], university)
        send_email(
            recipient=university["email"],
            subject=format_template(json["email"]['subject'], university),
            body_text=body_text,
            body_html=markdown(body_text)
        )

        break


if __name__ == "__main__":
    main()
