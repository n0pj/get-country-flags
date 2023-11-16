import os
import requests


def get_country_codes():
    # Opendatasoft の API から国コードのリストを取得する
    url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=countries-codes&q=&rows=300&facet=iso3166_1_alpha_2"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return [record['fields']['iso2_code'] for record in data['records']]


def download_flag(alpha2_code, directory):
    # Flagpedia.net API から国旗の画像を取得する URL
    url = f"https://flagcdn.com/h240/{alpha2_code.lower()}.png"

    try:
        response = requests.get(url)
        response.raise_for_status()

        # ディレクトリが存在しない場合は作成する
        if not os.path.exists(directory):
            os.makedirs(directory)

        # ファイル名を指定して画像を保存
        filename = os.path.join(directory, f"{alpha2_code}.png")
        with open(filename, 'wb') as file:
            file.write(response.content)

        return filename
    except requests.RequestException as e:
        # エラーログを記録する
        with open("download_errors.log", "a") as log_file:
            log_file.write(
                f"Error: alpha2_code {alpha2_code} is not found. {e}\n")
        return None


# 国コードのリストを取得し、各国の国旗を country_flags ディレクトリにダウンロード
country_codes = get_country_codes()
for code in country_codes:
    downloaded_file = download_flag(code, "country_flags")
    if downloaded_file:
        print(f"Downloaded: {downloaded_file}")
    else:
        print(f"Download failed: {code}")
