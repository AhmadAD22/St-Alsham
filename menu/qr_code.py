import qrcode

def generate_qr_code(username, wifi_ssid, wifi_password):
    # Format the WiFi details as a string
    wifi_details = f"WIFI:T:WPA;S:{wifi_ssid};P:{wifi_password};;"

    # Create a QR code instance
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
    qr.add_data(wifi_details)
    qr.make(fit=True)

    # Save the QR code as an image
    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_image.save(f"{username}_wifi_qr_code.png")