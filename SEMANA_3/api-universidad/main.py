from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import blockchain
import models
from database import Base, engine, get_db, wait_for_database
from schemas import CertificadoCrear, CertificadoRespuesta, VerificacionRespuesta


@asynccontextmanager
async def lifespan(app: FastAPI):
    wait_for_database()
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="API Minerales - Registro de Certificados de Exportacion",
    description="API para registrar certificados de exportacion de minerales en PostgreSQL y guardar evidencia en blockchain.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/blockchain/contract")
def blockchain_contract():
    try:
        exists = blockchain.verify_contract_exists()
        return {
            "contract_address": blockchain.get_contract_address(),
            "existe_en_blockchain": exists,
        }
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@app.post("/certificados", response_model=CertificadoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_certificado(payload: CertificadoCrear, db: Session = Depends(get_db)):
    codigo_certificado_hash = blockchain.hash_text(payload.codigo_certificado)
    documento_hash = blockchain.hash_text(payload.contenido_documento)

    certificado = models.Certificado(
        codigo_certificado=payload.codigo_certificado,
        empresa_exportadora=payload.empresa_exportadora,
        ruc_empresa=payload.ruc_empresa,
        tipo_mineral=payload.tipo_mineral,
        tipo_certificado=payload.tipo_certificado,
        entidad_emisora=payload.entidad_emisora,
        fecha_emision=payload.fecha_emision,
        contenido_documento=payload.contenido_documento,
        codigo_certificado_hash=codigo_certificado_hash,
        documento_hash=documento_hash,
        contract_address=blockchain.get_contract_address(),
    )

    db.add(certificado)

    try:
        tx_hash = blockchain.register_certificate(codigo_certificado_hash, documento_hash)
        certificado.tx_hash = tx_hash
        db.commit()
        db.refresh(certificado)
        return certificado
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un certificado con ese codigo",
        ) from error
    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(error)) from error


@app.get("/certificados/{codigo_certificado}", response_model=CertificadoRespuesta)
def obtener_certificado(codigo_certificado: str, db: Session = Depends(get_db)):
    certificado = db.query(models.Certificado).filter(
        models.Certificado.codigo_certificado == codigo_certificado
    ).first()

    if certificado is None:
        raise HTTPException(status_code=404, detail="Certificado no encontrado")

    return certificado


@app.get("/certificados/{codigo_certificado}/verificar", response_model=VerificacionRespuesta)
def verificar_certificado(codigo_certificado: str, db: Session = Depends(get_db)):
    certificado = db.query(models.Certificado).filter(
        models.Certificado.codigo_certificado == codigo_certificado
    ).first()

    if certificado is None:
        raise HTTPException(status_code=404, detail="Certificado no encontrado")

    try:
        existe, documento_coincide = blockchain.verify_certificate(
            certificado.codigo_certificado_hash,
            certificado.documento_hash,
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    return VerificacionRespuesta(
        codigo_certificado=certificado.codigo_certificado,
        codigo_certificado_hash=certificado.codigo_certificado_hash,
        documento_hash=certificado.documento_hash,
        existe_en_blockchain=existe,
        documento_coincide=documento_coincide,
        contract_address=certificado.contract_address,
    )
