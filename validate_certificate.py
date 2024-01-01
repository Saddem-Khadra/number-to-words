from pydantic import BaseModel


class CertificateInput(BaseModel):
    certificate_base64: str
