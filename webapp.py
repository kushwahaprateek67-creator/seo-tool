def make_email_html(body, sender, sender_email):
    safe_body = html.escape(body).replace("\n", "<br>")

    unsubscribe_url = (
        "mailto:"
        + quote(sender_email, safe="@.+-_")
        + "?subject=Unsubscribe"
    )

    return f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family:Arial,sans-serif;color:#222;">
        <div>{safe_body}</div>
        <br><br>
        <div>
            {html.escape(sender)}
            <br>
            <a href="{html.escape(unsubscribe_url, quote=True)}"
               style="color:#0878d1;text-decoration:underline;">
                Unsubscribe
            </a>
        </div>
    </body>
    </html>
    """
