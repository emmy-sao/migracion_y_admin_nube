import { network } from "hardhat";

const { viem } = await network.create();

console.log("Desplegando contrato RegistroCertificados...");

const registroCertificados = await viem.deployContract("RegistroCertificados");

console.log("Contrato desplegado correctamente");
console.log("Direccion del contrato:", registroCertificados.address);
