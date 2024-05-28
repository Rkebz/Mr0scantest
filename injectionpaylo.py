import http.client
import urllib.parse
import ssl

def inject_payload(url, parameters, payload, method='GET'):
    """
    حقن بايلود في موقع ويب معين
    Args:
        url (str): عنوان URL الكامل للموقع المستهدف (بما في ذلك البروتوكول مثل http أو https)
        parameters (dict): قاموس يحتوي على أسماء المعلمات وقيمها الأولية
        payload (str): بايلود الذي سيتم حقنه
        method (str): طريقة الطلب (GET أو POST)
    Returns:
        tuple: (status_code, response_data)
    """
    parsed_url = urllib.parse.urlparse(url)
    host = parsed_url.netloc
    path = parsed_url.path or '/'
    
    headers = {
        'User-Agent': 'Python HTTP Client'
    }

    if parsed_url.scheme == 'https':
        conn = http.client.HTTPSConnection(host, context=ssl._create_unverified_context())
    else:
        conn = http.client.HTTPConnection(host)

    if method.upper() == 'GET':
        injected_params = parameters.copy()
        for key in injected_params:
            injected_params[key] = payload
        query_string = urllib.parse.urlencode(injected_params)
        url_with_payload = f"{path}?{query_string}"
        conn.request("GET", url_with_payload, headers=headers)
    elif method.upper() == 'POST':
        post_data = parameters.copy()
        for key in post_data:
            post_data[key] = payload
        encoded_data = urllib.parse.urlencode(post_data)
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        conn.request("POST", path, body=encoded_data, headers=headers)
    else:
        return None, "Unsupported HTTP method. Use GET or POST."

    response = conn.getresponse()
    data = response.read().decode()
    conn.close()

    return response.status, data

def save_to_file(filename, data):
    """
    حفظ البيانات في ملف نصي
    Args:
        filename (str): اسم الملف
        data (str): البيانات التي يجب حفظها
    """
    with open(filename, 'a') as file:
        file.write(data)

def main():
    url = input("أدخل رابط الموقع المستهدف (بما في ذلك http أو https): ")

    # قراءة البايلودات من ملف النص
    with open("payloads.txt", "r") as f:
        payloads = f.readlines()
    payloads = [x.strip() for x in payloads]

    # إعداد المعلمات الافتراضية للاختبار. يمكن تعديلها بناءً على احتياجاتك.
    parameters = {
        "id": "1",
        "name": "test"
    }
    
    # تجربة الحقن باستخدام GET و POST
    methods = ['GET', 'POST']
    
    for method in methods:
        for payload in payloads:
            print(f"Testing payload: {payload} using {method}")
            status, result = inject_payload(url, parameters, payload, method=method)
            if status == 200 and "error" not in result.lower():
                print(f"Successful injection with payload: {payload}")
                print("Response data:")
                print(result)
                # حفظ البيانات في ملف
                save_to_file("results.txt", f"Payload: {payload}\nResponse: {result}\n\n")
                break
        else:
            continue
        break
    else:
        print("No successful payload found.")

if __name__ == "__main__":
    main()
