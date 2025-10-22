import time
import hmac
import hashlib
import base64
import requests


class SignatureGenerator:
    @staticmethod
    def hmac_sha256(var_39: bytes, var_40: bytes) -> str:
        try:
            # Equivalent to crypto.subtle.sign("HMAC", key, data)
            var_42 = hmac.new(var_39, var_40, hashlib.sha256).digest()
            # Equivalent to btoa(String.fromCharCode(...))
            return base64.b64encode(var_42).decode()
        except Exception as var_43:
            print("HMAC generation error:", var_43)
            return ""

    @staticmethod
    def generateSignature(var_33: str) -> str:
        try:
            var_34 = "q7D]325Xc&+lJ8XG~4(yiz2ub3"
            var_35 = var_33.encode()  # TextEncoder().encode(var_33)
            var_37 = var_34.encode()  # TextEncoder().encode(var_34)
            return SignatureGenerator.hmac_sha256(var_37, var_35)
        except Exception as var_38:
            print("Signature generation error:", var_38)
            return ""

    @staticmethod
    def generateProtectionSignature(var_44: str) -> str:
        try:
            var_45 = "uB2n%*sir[&*k2UO£>h8jZ6m$)0@kZf>"
            var_46 = "3,9_(@58F5YCq%kz"
            var_47 = var_45 + var_46 + var_44
            var_49 = var_45.encode()  # TextEncoder().encode(var_45)
            var_50 = var_47.encode()  # TextEncoder().encode(var_47)
            var_52 = hmac.new(var_49, var_50, hashlib.sha256).digest()
            return base64.b64encode(var_52).decode()
        except Exception as var_53:
            print("Protection signature generation error:", var_53)
            return ""


def get_data(page: int):
    try:
        var_54 = str(int(time.time()))
        var_55 = SignatureGenerator.generateSignature(var_54)
        var_56 = SignatureGenerator.generateProtectionSignature(var_54)

        api = f"https://streamfiles.eu.org/api/fetch_filters.php?filterType=all_batches&page={page}"

        headers = {
            "Cache-Control": "",
            "Accept": "application/json",
            "dev-jisu-key": var_54,
            "dev-jisu-protection-signature": var_56,
            "dev-jisu-signature": var_55
        }

        res = requests.get(api, headers=headers)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print("Error fetching data:", e)
        return None
print(get_data(1))
