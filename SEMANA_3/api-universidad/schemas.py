from datetime import date, datetime

from pydantic import BaseModel, Field


class CertificadoCrear(BaseModel):
    codigo_certificado: str = Field(examples=["ARCOM-ORO-2026-0001"])
    empresa_exportadora: str = Field(examples=["Lundin Gold"])
    ruc_empresa: str = Field(examples=["1792345678001"])
    tipo_mineral: str = Field(examples=["Oro"])
    tipo_certificado: str = Field(examples=["Certificado de Exportacion de Minerales"])
    entidad_emisora: str = Field(default="ARCOM", examples=["ARCOM"])
    fecha_emision: date = Field(examples=["2026-06-15"])
    contenido_documento: str = Field(
        examples=["Certificado de exportacion de mineral Oro emitido por ARCOM a Lundin Gold RUC 1792345678001"]
    )


class CertificadoRespuesta(BaseModel):
    id: int
    codigo_certificado: str
    empresa_exportadora: str
    ruc_empresa: str
    tipo_mineral: str
    tipo_certificado: str
    entidad_emisora: str
    fecha_emision: date
    codigo_certificado_hash: str
    documento_hash: str
    contract_address: str
    tx_hash: str | None
    creado_en: datetime

    model_config = {"from_attributes": True}


class VerificacionRespuesta(BaseModel):
    codigo_certificado: str
    codigo_certificado_hash: str
    documento_hash: str
    existe_en_blockchain: bool
    documento_coincide: bool
    contract_address: str
