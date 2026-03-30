import msal

CLIENT_ID = "f8249dbf-3729-4b8f-ba05-172b60aab6fd" 

app = msal.PublicClientApplication(
    CLIENT_ID, 
    authority="https://login.microsoftonline.com/consumers"
)

# ¡Le quitamos el offline_access porque MSAL ya lo pide por defecto!
flow = app.initiate_device_flow(scopes=["Files.ReadWrite"])

if "user_code" not in flow:
    print("Error iniciando el flujo:", flow)
    exit()

print("\n" + "="*50)
print(flow["message"])
print("="*50 + "\n")

result = app.acquire_token_by_device_flow(flow)

if "refresh_token" in result:
    print("\n✅ ¡ÉXITO! Copia este texto gigante, es tu MICROSOFT_REFRESH_TOKEN:\n")
    print(result["refresh_token"])
else:
    print("\n❌ Error:", result.get("error_description", result))