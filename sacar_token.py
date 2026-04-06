import msal
 
CLIENT_ID = "7bf50050-0533-42d2-a955-ffbf7930b154"
TENANT_ID = "513294a0-3e20-41b2-a970-6d30bf1546fa"
 
app = msal.PublicClientApplication(
    CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{TENANT_ID}"
)
 
print("Abriendo el navegador para validar tu computadora corporativa...")
 
result = app.acquire_token_interactive(scopes=["Files.ReadWrite"])
 
if "refresh_token" in result:
    print("\n✅ ¡ÉXITO! Copia este texto gigante, es tu MICROSOFT_REFRESH_TOKEN:\n")
    print(result["refresh_token"])
else:
    print("\n❌ Error:", result.get("error_description", result))