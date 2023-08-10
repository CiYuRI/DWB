import requests

def fetch_proxies():
    https_urls = [
        'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt',
        'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt',
        'https://raw.githubusercontent.com/yoannchb-pro/https-proxies/main/proxies.txt',
        'https://raw.githubusercontent.com/aslisk/proxyhttps/main/https.txt',
    ]
    
    http_urls = [
        'https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/free.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/http.txt',
        'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt',
        'https://raw.githubusercontent.com/yoannchb-pro/https-proxies/main/proxies.txt',
        'https://raw.githubusercontent.com/Bardiafa/Proxy-Leecher/main/good.txt',
    ]

    https_proxies = []
    for url in https_urls:
        response = requests.get(url)
        if response.status_code == 200:
            https_proxies += [proxy.strip() for proxy in response.text.splitlines()]
        else:
            print(f"Failed to fetch HTTPS proxies from {url}. Status code: {response.status_code}")

    http_proxies = []
    for url in http_urls:
        response = requests.get(url)
        if response.status_code == 200:
            http_proxies += [proxy.strip() for proxy in response.text.splitlines()]
        else:
            print(f"Failed to fetch HTTP proxies from {url}. Status code: {response.status_code}")

    if not https_proxies and not http_proxies:
        print("Failed to fetch any proxies. Exiting.")
        exit()

    return https_proxies, http_proxies