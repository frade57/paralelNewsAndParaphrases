_apiKeys = ['914dc5ed8630430c83faf11042fd132f', 'b4c4724a58c74b70bd0770ec10aef963'
            ,'b4d79bca2afc46cca689a9d56191de96','e1d5cc56f2a0416b89f96a4674376509'
            ,'ec884b06a14c48d5a228eedb974a0d16','c169939a32034a3185d1f51d034b9a76'
            ,'335e3421dcf44c89a6b1139e1cd0d0fa','7e242aef54a0477a80d5321fe2f4b8a8'
            ,'65439ebf79774eafa808c89734098338','c8833a7fadbf42b9bf394e65ac3980e4'
            ,'d93813897d4a4520830678cfa27e088d','0bfbb6ee571c4f3696e6951f61e8db7e'
            ,'5813d27253c4434399c72d23924917da','94c9e676774c4bc5b1eb413ffc97e67a'
            ,'e56c647f910a4ddd827ea8a59124db33','95ae48aa8f944257bb6e6dbddfb11bd8'
            ,'28ba5b51df2b4f71ab29f7d94d5900d8','c34cc55899014f5d9c09f3cf5b3f10f3'
            ,'872e10ba3db44a4c8daa4dde9ef659a3','680bce9f597f4c5da6574dc3eee251f0'
            ,'da12e78b51ec45f9a90f828156118d2c','eb96f75f235d46f783780f8bb1955a76'
            ,'dff1dd6dd66e4ec891d11ed6738639f1','049e7b7ebabd4508b547f7a2bfc9b8b3'
            ,'4fdeaba15e2f4d7bbeac6cc865a57ee0','d906645877fe4bb6a15012144f14e9ff']
_currentApiKeyIndex = 1
_apiKey = _apiKeys[_currentApiKeyIndex]

def changeApiKey():

    global _apiKey
    global _currentApiKeyIndex

    _apiKey = _apiKeys[(_currentApiKeyIndex + 1) % len(_apiKeys)] # / % para voltar a 1º pos
    _currentApiKeyIndex = (_currentApiKeyIndex + 1) % len(_apiKeys)

