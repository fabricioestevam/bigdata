import socket
import subprocess

def test_network():
    print("🌐 Testando conectividade de rede...")
    
    try:
        # Testar DNS
        socket.gethostbyname('cluster0.wnfcroh.mongodb.net')
        print("✅ DNS funcionando")
    except:
        print("❌ DNS não resolve")
    
    # Testar ping (pode não funcionar em todos os ambientes)
    try:
        result = subprocess.run(['ping', '-c', '1', 'google.com'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Conexão de rede OK")
        else:
            print("⚠️  Possível problema de rede")
    except:
        print("⚠️  Não foi possível testar ping")

test_network()
