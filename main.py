import requests
import json
import random
import time
from concurrent.futures import ThreadPoolExecutor
from helpers.prx import fetch_proxies
from helpers.plrd import update_payload
import streamlit as st

st.title("Sayaka's DWB")

webhook_url = st.text_input("Webhook URL:")
message_content = st.text_input("Message content:")

num_requests = st.number_input("Enter the number of requests to make (between 1 and 1000):", min_value=1, max_value=1000, value=100)

https_proxies, http_proxies = fetch_proxies()

if webhook_url == '' or message_content == '':
    st.warning("Please fill in all the input boxes.")
elif num_requests < 1 or num_requests > 1000:
    st.warning("Please enter a value between 1 and 1000 for the number of requests.")
else:
    if st.button(f"Fetched a total of {len(https_proxies) + len(http_proxies)} proxies. Proceed with {num_requests} requests?", key="proceed"):
        progress_bar = st.progress(0)
        stop_button = st.button("Stop")

        with st.spinner("Sending requests, please wait..."):
            with ThreadPoolExecutor(max_workers=len(https_proxies) + len(http_proxies)) as executor:
                futures = []
                success_count = 0
                rate_limit_count = 0

                session = requests.Session()

                for i in range(num_requests):
                    name, pfp_url = update_payload()

                    payload = {
                        "content": message_content,
                        "username": name,
                        "avatar_url": pfp_url
                    }

                    if i % 2 == 0:
                        proxies = https_proxies
                        protocol = 'https'
                    else:
                        proxies = http_proxies
                        protocol = 'http'

                    proxy = random.choice(proxies)
                    while True:
                        try:
                            future = executor.submit(session.post, webhook_url, json=payload, proxies={protocol: proxy}, timeout=10)
                            futures.append(future)
                            break
                        except requests.exceptions.Timeout:
                            proxy = random.choice(proxies)
                            continue
                        except:
                            proxy = random.choice(proxies)
                            continue
                    if (i + 1) % 49 == 0:
                        time.sleep(1)
                    progress_bar.progress((i+1)/num_requests)

                    if stop_button:
                        break

                for future in futures:
                    try:
                        response = future.result()
                        if response.status_code == 204:
                            success_count += 1
                        elif response.status_code == 429:
                            rate_limit_count += 1
                    except requests.exceptions.Timeout:
                        continue
                    except:
                        continue

        st.success(f"Successful requests: {success_count}")
        st.warning(f"Rate-limited requests: {rate_limit_count}")
    else:
        st.warning("Please click the button to proceed.")