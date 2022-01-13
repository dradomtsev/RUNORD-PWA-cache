import logging
import os
import requests
from xml.etree import ElementTree

# %%
def pwa_cookie_auth():
    binary_secrurity_token  = get_pwa_bin_sec_token()
    cookies                 = get_pwa_auth_cookies(binary_secrurity_token)
    return cookies

# %%

def get_pwa_bin_sec_token():
    url = 'https://login.microsoftonline.com/extSTS.srf'
    body = '<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://www.w3.org/2005/08/addressing" xmlns:u="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd"><s:Header><a:Action s:mustUnderstand="1">http://schemas.xmlsoap.org/ws/2005/02/trust/RST/Issue</a:Action><a:ReplyTo><a:Address>http://www.w3.org/2005/08/addressing/anonymous</a:Address></a:ReplyTo><a:To s:mustUnderstand="1">https://login.microsoftonline.com/extSTS.srf</a:To><o:Security xmlns:o="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" s:mustUnderstand="1"><o:UsernameToken><o:Username>'+os.environ["PWA_USER_LOGIN"]+'</o:Username><o:Password>'+os.environ["PWA_USER_PASS"]+'</o:Password></o:UsernameToken></o:Security></s:Header><s:Body><t:RequestSecurityToken xmlns:t="http://schemas.xmlsoap.org/ws/2005/02/trust"><wsp:AppliesTo xmlns:wsp="http://schemas.xmlsoap.org/ws/2004/09/policy"><a:EndpointReference><a:Address>https://archimatika.sharepoint.com</a:Address></a:EndpointReference></wsp:AppliesTo><t:KeyType>http://schemas.xmlsoap.org/ws/2005/05/identity/NoProofKey</t:KeyType><t:RequestType>http://schemas.xmlsoap.org/ws/2005/02/trust/Issue</t:RequestType><t:TokenType>urn:oasis:names:tc:SAML:1.0:assertion</t:TokenType></t:RequestSecurityToken></s:Body></s:Envelope>'

    response = requests.post(url, data=body)

    response = ElementTree.fromstring(response.content)
    binary_secrurity_token = response.find(
        './/{http://www.w3.org/2003/05/soap-envelope}Body/{http://schemas.xmlsoap.org/ws/2005/02/trust}RequestSecurityTokenResponse/{http://schemas.xmlsoap.org/ws/2005/02/trust}RequestedSecurityToken/{http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd}BinarySecurityToken').text

    return binary_secrurity_token

# %%

def get_pwa_auth_cookies(binary_secrurity_token):
    url = 'https://'+os.environ["PWA_DOMAIN_NAME"]+'/_forms/default.aspx?wa=wsignin1.0'
    body = binary_secrurity_token

    response = requests.post(url, data=body)
    cookies = []
    cookies.append(response.cookies['rtFa'])
    cookies.append(response.cookies['FedAuth'])
    return cookies