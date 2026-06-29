// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract RegistroCertificados {
    struct Certificado {
        bytes32 codigoCertificadoHash;
        bytes32 documentoHash;
        address entidadEmisora;
        uint256 fechaRegistro;
        bool existe;
    }

    mapping(bytes32 => Certificado) private certificados;

    event CertificadoRegistrado(
        bytes32 indexed codigoCertificadoHash,
        bytes32 indexed documentoHash,
        address indexed entidadEmisora
    );

    function registrarCertificado(
        bytes32 codigoCertificadoHash,
        bytes32 documentoHash
    ) public {
        require(!certificados[codigoCertificadoHash].existe, "El certificado ya existe");

        certificados[codigoCertificadoHash] = Certificado({
            codigoCertificadoHash: codigoCertificadoHash,
            documentoHash: documentoHash,
            entidadEmisora: msg.sender,
            fechaRegistro: block.timestamp,
            existe: true
        });

        emit CertificadoRegistrado(codigoCertificadoHash, documentoHash, msg.sender);
    }

    function verificarCertificado(
        bytes32 codigoCertificadoHash,
        bytes32 documentoHash
    ) public view returns (bool existe, bool documentoCoincide) {
        Certificado memory cert = certificados[codigoCertificadoHash];
        existe = cert.existe;
        documentoCoincide = cert.documentoHash == documentoHash;
    }

    function obtenerCertificado(
        bytes32 codigoCertificadoHash
    ) public view returns (bytes32, bytes32, address, uint256, bool) {
        Certificado memory cert = certificados[codigoCertificadoHash];
        return (
            cert.codigoCertificadoHash,
            cert.documentoHash,
            cert.entidadEmisora,
            cert.fechaRegistro,
            cert.existe
        );
    }
}
