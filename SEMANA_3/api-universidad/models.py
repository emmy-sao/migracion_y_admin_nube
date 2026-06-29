from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Certificado(Base):
    __tablename__ = "certificados"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    codigo_certificado: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    empresa_exportadora: Mapped[str] = mapped_column(String(200))
    ruc_empresa: Mapped[str] = mapped_column(String(50), index=True)
    tipo_mineral: Mapped[str] = mapped_column(String(200))
    tipo_certificado: Mapped[str] = mapped_column(String(200))
    entidad_emisora: Mapped[str] = mapped_column(String(200), default="ARCM")
    fecha_emision: Mapped[date] = mapped_column(Date)
    contenido_documento: Mapped[str] = mapped_column(Text)
    codigo_certificado_hash: Mapped[str] = mapped_column(String(66), index=True)
    documento_hash: Mapped[str] = mapped_column(String(66), index=True)
    contract_address: Mapped[str] = mapped_column(String(42))
    tx_hash: Mapped[str | None] = mapped_column(String(66), nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
