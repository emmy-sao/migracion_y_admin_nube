import { network } from "hardhat";
import { keccak256, stringToHex } from "viem";

const { viem } = await network.create();

console.log("Desplegando contrato RegistroCertificados...");

const registroCertificados = await viem.deployContract("RegistroCertificados");

console.log("Contrato desplegado en:", registroCertificados.address);

const codigoCertificado = "ARCM-ORO-2026-0001";
const contenidoDocumento =
  "Certificado de exportacion de mineral Oro emitido por ARCM a Minera Ecuatoriana S.A. RUC 1792345678001";

const codigoCertificadoHash = keccak256(stringToHex(codigoCertificado));
const documentoHash = keccak256(stringToHex(contenidoDocumento));

console.log("Codigo del certificado:", codigoCertificado);
console.log("Hash del codigo:", codigoCertificadoHash);
console.log("Hash del documento:", documentoHash);

console.log("Registrando certificado en blockchain...");

const tx = await registroCertificados.write.registrarCertificado([
  codigoCertificadoHash,
  documentoHash,
]);

console.log("Transaccion enviada:", tx);

const resultado = await registroCertificados.read.verificarCertificado([
  codigoCertificadoHash,
  documentoHash,
]);

console.log("Resultado de verificacion:");
console.log("Existe:", resultado[0]);
console.log("Documento coincide:", resultado[1]);

const certificado = await registroCertificados.read.obtenerCertificado([codigoCertificadoHash]);

console.log("Datos guardados en blockchain:");
console.log("codigoCertificadoHash:", certificado[0]);
console.log("documentoHash:", certificado[1]);
console.log("entidadEmisora:", certificado[2]);
console.log("fechaRegistro:", certificado[3]);
console.log("existe:", certificado[4]);
