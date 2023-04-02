import socket
import requests
import re
import time
from bs4 import BeautifulSoup
from termcolor import colored

logo = "\033[38;2;0;255;255m" + """
██████╗░░█████╗░████████╗░█████╗░░█████╗░██████╗░
██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗╚════██╗
██║░░██║███████║░░░██║░░░███████║██║░░╚═╝░█████╔╝
██║░░██║██╔══██║░░░██║░░░██╔══██║██║░░██╗░╚═══██╗
██████╔╝██║░░██║░░░██║░░░██║░░██║╚█████╔╝██████╔╝
╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░╚═════╝░""" + "\033[0m"

author = colored("Created By Raunchy#7256 and dgknsygn", "blue")

print("\n")
for i, line in enumerate(logo.split("\n")):
    color = "cyan" if i == 0 else "yellow" if i % 2 == 0 else "green"
    print(colored(line, color))

print("\n" + author)

toolOneText = colored("[1] Uzantı Tarayıcı", "cyan")
toolTwoText = colored("[2] IP Bulucu", "yellow")
toolThreeText = colored("[3] Port Tarayıcı", "magenta")
toolFourText = colored("[4] Discord Bombalayıcı", "cyan")
toolFiveText = colored("[5] XSS Tarayıcı", "yellow")

print("\n", toolOneText, "\n", toolTwoText, "\n", toolThreeText, "\n", toolFourText, "\n", toolFiveText, "\n")

SelectNumber = int(input("[?] Araç Numarası: "))
    
if SelectNumber == 1:
    def get_extensions():
        url = input("\n" + colored("Uzantıları bulmak istediğiniz sitenin URL'sini girin: ", "green")).rstrip('0')

        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(colored("Hata: ", "red") + str(e))
            return

        soup = BeautifulSoup(response.text, "html.parser")
        links = [link.get("href") for link in soup.find_all("a")]
         
        extensions = set()
        for link in links:
            if link:
                extension = link.split(".")[-1]
                extensions.add(extension)

        result_title = colored("\nBu siteye ait tüm uzantılar:", "yellow")
        print(result_title)
        print("=" * len(result_title))

        for i, ext in enumerate(extensions):
            color = "magenta" if i % 2 == 0 else "cyan"
            print(colored("[+] ", color) + ext)

        print("=" * len(result_title))

    FirstTime = True

    while True:
        if FirstTime: 
            get_extensions()
            FirstTime = False
    	
        ask = input(colored("Yeniden başlatmak ister misiniz? [Y/N]: ", "yellow"))
        if ask.lower() == "y":
    	    get_extensions()
        elif ask.lower() == "n":
            break
        else:
    	    print("Lütfen [Y/N] dışında bir şey yazmayın!")

    input(colored("Program sonlandırıldı. Çıkmak için ENTER tuşuna basın.", "red"))
elif SelectNumber == 2:
    def ip_bul(url):
        try:
            ip_adresi = socket.gethostbyname(url)
            return f"{url} sitesinin IP adresi: {ip_adresi}"
        except:
            return "IP adresi bulunamadı."

    while True:
        url = input(colored("\nLütfen IP adresini bulmak istediğiniz web sitesinin URL'sini girin: ", "yellow"))
        print(ip_bul(url))
elif SelectNumber == 3:
    def port_tara(ip, aralik):
        try:
            port_araligi = aralik.split("-")
            port_range = range(int(port_araligi[0]), int(port_araligi[1])+1)

            for port in port_range:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    print(f"Port {port} açık")
                else:
                    print(f"Port {port} kapalı")
                sock.close()
        except:
            return "Tarama esnasında bir sorun çıktı!"

    while True:
        ip = input(colored("\nLütfen taramak istediğiniz IP adresini girin: ", "magenta"))
        aralik = input("Port tarama aralığı (80-443): ")
        port_tara(ip, aralik)
        
elif SelectNumber == 4:
    webhook_url = input(colored("\nWebhook URL'si girin: ", "cyan"))
    bot_username = input(colored("Bot kullanıcı adını girin: ", "cyan"))
    avatar_url = input(colored("Avatar URL'sini girin (boş bırakmak için Enter'a basın): ", "cyan"))
    message_text = input(colored("Gönderilecek mesajı girin: ", "cyan"))
    message_count = input(colored("Gönderilecek mesaj sayısı: ", "cyan"))


    message = {
        "username": bot_username,
        "content": message_text
    }

    if avatar_url:
        message["avatar_url"] = avatar_url

    for i in range(message_count):
        response = requests.post(webhook_url, json=message)
        if response.status_code == 204:
       	    print("Webhook gönderildi! ({}/{})".format(i+1, message_count))
        else:
            print("Webhook gönderilemedi. ({}/{})".format(i+1, message_count))
        
        time.sleep(1)
        
elif SelectNumber == 5:
    def xss_tarama(url):
        try:
            response = requests.get(url)
            # Formları bul
            forms = re.findall(r'<form.*?>.*?</form>', response.text, flags=re.DOTALL)
            for form in forms:
            
                inputs = re.findall(r'<input.*?>', form)
                for input_tag in inputs:
                
                    input_name = re.findall(r'name=["\'](.*?)["\']', input_tag)[0]
               
                    payload = '<script>alert(1)</script>'
               
                    form = form.replace(input_tag, input_tag.replace('>', 'value="{}">'.format(payload)))
              
                    response = requests.post(url, data=form)
                
                    if payload in response.text:
                        print('XSS açığı bulundu. Form: "{}", Input adı: "{}"'.format(form, input_name))
        except Exception as e:
            print('Hata:', e)
            
    url = input(colored("\nLütfen taranacak site adresini giriniz: ", "yellow"))
    print(xss_tarama(url))

else:
    print(colored("\nLütfen belirtilen haricinde bir şey yazmayın [1-5]", "red"))
