import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor
from helpers.prx import fetch_proxies
from helpers.plrd import uwupayload, chadpayload
import streamlit as st


def is_valid_webhook_url(url: str) -> bool:
    return url.startswith("https://discord.com/api/webhooks/")


def check_webhook_url(webhook_url: str) -> bool:
    try:
        response = requests.get(webhook_url, timeout=10)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


st.title("Sayaka's DWB")
webhook_url = st.text_input("**Webhook URL:**")
if not is_valid_webhook_url(webhook_url):
    st.warning("Please enter a valid Discord webhook URL.")
else:
    with st.spinner("Checking webhook URL..."):
        if check_webhook_url(webhook_url):
            st.success("Webhook URL is valid")
            https_proxies, http_proxies = fetch_proxies()
            st.divider()
            st.subheader("Payload Config")
            include_everyone = st.selectbox(
                "**Ping options:**", ["None", "@everyone", "@here"]
            )
            message_content = st.text_input("**Message content:**")
            names_func = st.selectbox("**Profile options**", ["UwU", "Chad", "Custom"])
            if names_func == "Custom":
                custom_username = st.text_input("**Username:**")
                custom_avatar_url = st.text_input("**Avatar URL:**")
            else:
                custom_username = None
                custom_avatar_url = None
            delete_webhook = st.checkbox("Delete webhook after sending requests")
            st.divider()
            num_requests = st.slider(
                "**Number of requests:**", min_value=1, max_value=1000, value=100
            )
            if message_content == "" or num_requests < 1 or num_requests > 1000:
                st.warning("Please fill in all of the options.")
            elif st.button(f"Proceed with {num_requests} requests?", key="proceed"):
                progress_bar = st.progress(0)
                stop_button = st.button("Stop")
                with st.spinner("Sending requests, please wait..."):
                    with ThreadPoolExecutor(
                        max_workers=len(https_proxies) + len(http_proxies)
                    ) as executor:
                        futures = []
                        success_count = 0
                        rate_limit_count = 0
                        session = requests.Session()
                        for i in range(num_requests):
                            if names_func == "Custom":
                                name = custom_username
                                pfp_url = custom_avatar_url
                            elif names_func == "UwU":
                                name, pfp_url = uwupayload()
                            else:
                                name, pfp_url = chadpayload()
                            if include_everyone == "@everyone":
                                message_content_with_everyone = (
                                    "@everyone " + message_content
                                )
                            elif include_everyone == "@here":
                                message_content_with_everyone = (
                                    "@here " + message_content
                                )
                            else:
                                message_content_with_everyone = message_content
                            payload = {
                                "content": message_content_with_everyone,
                                "username": name,
                                "avatar_url": pfp_url,
                            }
                            proxies = https_proxies if i % 2 == 0 else http_proxies
                            protocol = "https" if i % 2 == 0 else "http"
                            proxy = random.choice(proxies)
                            while True:
                                try:
                                    future = executor.submit(
                                        session.post,
                                        webhook_url,
                                        json=payload,
                                        proxies={protocol: proxy},
                                        timeout=10,
                                    )
                                    futures.append(future)
                                    break
                                except:
                                    proxy = random.choice(proxies)
                                    continue
                            if (i + 1) % 49 == 0:
                                time.sleep(1)
                            progress_bar.progress((i + 1) / num_requests)
                            if stop_button:
                                break
                        for future in futures:
                            try:
                                response = future.result()
                                if response.status_code == 204:
                                    success_count += 1
                                elif response.status_code == 429:
                                    rate_limit_count += 1
                            except:
                                continue
                    st.success(f"Successful requests: {success_count}")
                    st.warning(f"Rate-limited requests: {rate_limit_count}")
                    if delete_webhook:
                        headers = {"Content-Type": "application/json"}
                        response = requests.delete(webhook_url, headers=headers)
                        if response.status_code == 204:
                            st.success("Webhook deleted successfully")
                        elif response.status_code == 404:
                            st.warning("Webhook does not exist")
                        else:
                            st.error(f"Error deleting webhook: {response.text}")
            else:
                st.warning("Please click the button to proceed.")
        else:
            st.warning("Webhook URL is invalid.")


st.divider()
st.subheader("Help Section")
expander = st.expander("What is this DWB?")
expander.write(
    "This DWB (Discord Webhook Bomber) is a tool that allows you to send multiple requests to a Discord webhook, while avoiding the typical ratelimiting limits. The creator is not responsible for any misuse or damage. Please use this tool responsibly and to help take down scammers!"
)
expander = st.expander("Why isn't my webhook working?")
expander.write(
    "The DWB implements two checks; one for a correctly formatted Discord API URL, and another for a valid Discord webhook. If your webhook is not working, please check that you have entered the correct URL. If you are sure that you have entered the correct URL, then your webhook may have been deleted or is invalid."
)

expander = st.expander("How do I configure the ping options?")
expander.write(
    'Selecting "None" will not ping anyone. Selecting "@everyone" will ping everyone in the server. Selecting "@here" will only ping everyone that is currently online. Defaults to "None" automatically.'
)

expander = st.expander("How do I configure the message content?")
expander.write("Type in the message you want to send! It's pretty simple, really.")

expander = st.expander("What are profile options?")
expander.write(
    'The profile options are the name and avatar that will be used for the webhook. The "UwU" option will use cute names and anime avatars. The "Chad" option will use an alpha male name and avatar. The custom option will allow you to enter your own name and avatar URL. Defaults to "UwU" automatically.'
)

expander = st.expander(
    'What does the "Delete webhook after sending requests" option do?'
)
expander.write(
    'After sending your messages, the DWB will delete the webhook. This is useful if you want to send a lot of messages to a webhook, and then want to end the scamming. Defaults to "Disabled" automatically.'
)

expander = st.expander("How do I configure the number of requests?")
expander.write(
    "Due to discord security, not all requests will go through. Approximately only around 40 out of 500 requests will succeed."
)

expander = st.expander("Why is this site sometimes so d*mn buggy?")
expander.write(
    "Streamlit as a platform has its own limitations, and also this is still a work in progress. Rest assured the site will continue to improve over time!"
)
