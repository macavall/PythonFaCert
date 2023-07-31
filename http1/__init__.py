import logging
# load OpenSSL.crypto
from OpenSSL import crypto
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    xarr = req.headers.get("X-ARR-ClientCert")
    
    logging.info("==========X-ARR-ClientCert==============")
    logging.info(xarr)
    logging.info("==========X-ARR-ClientCert==============")

    
    # open it, using password. Supply/read your own from stdin.
    p12 = crypto.load_pkcs12(open("/var/ssl/private/E0F895B3D3344DD3B10183784832CD4827584F13.p12", "rb").read(), b"")
    
    # get various properties of said file.
    # note these are PyOpenSSL objects, not strings although you
    # can convert them to PEM-encoded strings.
    p12.get_certificate()     # (signed) certificate object
    logging.info(p12.get_certificate().get_issuer())      # private key.
    p12.get_ca_certificates() # ca chain.

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
