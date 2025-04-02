import requests

def solve_captcha(session, page_content):
    soup = BeautifulSoup(page_content, "html.parser")
    captcha_img = soup.find("img", {"id": "ContentPlaceHolder1_imgCaptcha"})
    if captcha_img:
        img_url = "https://tax.gov.ae" + captcha_img["src"]
        # Download image
        img_data = session.get(img_url).content
        # Send to 2Captcha (requires API key)
        api_key = "your-2captcha-api-key"
        response = requests.post(
            "http://2captcha.com/in.php",
            data={"key": api_key, "method": "base64", "body": img_data}
        )
        captcha_id = response.text.split("|")[1]
        # Get result
        result = requests.get(f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}")
        return result.text.split("|")[1]
    return None
