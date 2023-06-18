class ReturnFile:

    def header(self, data):
        dic_header = {
            "TIPO_DE_REGISTRO": data.get("TIPO_DE_REGISTRO"),
            "CODIGO_DE_RETORNO": data.get("CODIGO_DE_RETORNO"),
            "LITERAL_DE_RETORNO": data.get("LITERAL_DE_RETORNO"),
            "CODIGO_DO_SERVICO": data.get("CODIGO_DO_SERVICO"),
            "LITERAL_DE_SERVICO": data.get("LITERAL_DE_SERVICO"),
            "ISPB_PARTICIPANTE": data.get("ISPB_PARTICIPANTE"),
            "TIPO_DE_PESSOA_RECEBEDOR": data.get("TIPO_DE_PESSOA_RECEBEDOR"),
            "CPF_CNPJ": data.get("CPF_CNPJ"),
            "AGENCIA": data.get("AGENCIA"),
            "CONTA": data.get("CONTA"),
            "TIPO_CONTA": data.get("TIPO_CONTA"),
            "CHAVE_PIX": data.get("CHAVE_PIX"),
            "DATA_DE_GERACAO": data.get("DATA_DE_GERACAO"),
            "CODIGO_DO_CONVENIO": data.get("CODIGO_DO_CONVENIO"),
            "EXCLULSIVO_PSP_RECEBEDOR": data.get("EXCLULSIVO_PSP_RECEBEDOR"),
            "NOME_DO_RECEBEDOR": data.get("NOME_DO_RECEBEDOR"),
            "CODIGOS_DE_ERROR": data.get("CODIGOS_DE_ERROR"),
            "BRANCOS": data.get("BRANCOS"),
            "NUMERO_SEQUENCIAL_DO_RETORNO": data.get("NUMERO_SEQUENCIAL_DO_RETORNO"),
            "VERSAO_DO_ARQUIVO": data.get("VERSAO_DO_ARQUIVO"),
            "NUMERO_SEQUENCIASL_DO_REGISTRO": data.get("NUMERO_SEQUENCIASL_DO_REGISTRO"),
        }
        return dic_header

    def detalhe(self, list_data):
        list_detalhe = []
        for data in list_data:
            dic_detalhe = {
                "TIPO_DE_REGISTRO": data.get("TIPO_DE_REGISTRO"),
                "IDENTIFICADOR": data.get("IDENTIFICADOR"),
                "TIPO_DE_PESSOA_RECEBEDOR": data.get("TIPO_DE_PESSOA_RECEBEDOR"),
                "CPF_CNPJ": data.get("CPF_CNPJ"),
                "AGENCIA": data.get("AGENCIA"),
                "CONTA": data.get("CONTA"),
                "TIPO": data.get("TIPO"),
                "CHAVE_PIX": data.get("CHAVE_PIX"),
                "TIPO_COBRANCA": data.get("TIPO_COBRANCA"),
                "COD_DO_MOVIMENTO": data.get("COD_DO_MOVIMENTO"),
                "TIMESTAMP_EXPIRACAO": data.get("TIMESTAMP_EXPIRACAO"),
                "DATA_DE_VENCIMENTO": data.get("DATA_DE_VENCIMENTO"),
                "VALIDADE_APOS_VENCIMENTO": data.get("VALIDADE_APOS_VENCIMENTO"),
                "VALOR_ORIGINAL": data.get("VALOR_ORIGINAL"),
                "TIPO_DE_PESSOA_DEVEDOR": data.get("TIPO_DE_PESSOA_DEVEDOR"),
                "CPFCNPJ_DEVEDOR": data.get("CPFCNPJ_DEVEDOR"),
                "NOME_DEVEDOR": data.get("NOME_DEVEDOR"),
                "SOLICITACAO_AO_PAGADOR_OU_CAMPO_TEXTO_LIVRE": data.get("SOLICITACAO_AO_PAGADOR_OU_CAMPO_TEXTO_LIVRE"),
                "EXCLUSIVO_PSP_RECEBEDOR": data.get("EXCLUSIVO_PSP_RECEBEDOR"),
                "DATA_DE_MOVIMENTO": data.get("DATA_DE_MOVIMENTO"),
                "CODIGOS_DE_ERROR": data.get("CODIGOS_DE_ERROR"),
                "REVISAO": data.get("REVISAO"),
                "TARIFA_DE_COBRANCA": data.get("TARIFA_DE_COBRANCA"),
                "BRANCOS": data.get("BRANCOS"),
                "NUMERO_SEQUENCIAL": data.get("NUMERO_SEQUENCIAL"),
                "REGISTRO_DETALHE_INFORMACOES_ADICIONAIS": self.registro_detalhe_informacoes_adicionais(data.get("REGISTRO_DETALHE_INFORMACOES_ADICIONAIS")),
            }
            list_detalhe.append(dic_detalhe)
        return list_detalhe

    def registro_detalhe_informacoes_adicionais(self, list_info_adicionais):
        list_detalhe = []
        for data in list_info_adicionais:
            dic_detalhe = {
                "TIPO_DE_REGISTRO": data.get("TIPO_DE_REGISTRO"),
                "IDENTIFICADOR": data.get("IDENTIFICADOR"),
                "LISTA": [self.__nome_valor(data)],
                "BRANCOS": data.get("BRANCOS"),
                "NUMERO_SEQUENCIAL": data.get("NUMERO_SEQUENCIAL"),
            }
            list_detalhe.append(dic_detalhe)
        return list_detalhe

    def __nome_valor(self, list_nome_valor):
        list_detalhe = []
        for data in list_nome_valor:
            dic_detalhe = {
                "NOME": data.get("NOME"),
                "VALOR": data.get("VALOR"),
            }
            list_detalhe.append(dic_detalhe)
        return list_detalhe
    def emv(self, data):
        dic_emv = {
            "TIPO_DE_REGISTRO": data.get("TIPO_DE_REGISTRO"),
            "IDENTIFICADOR": data.get("IDENTIFICADOR"),
            "CHAVE_PIX": data.get("CHAVE_PIX"),
            "COD_DO_MOVIMENTO": data.get("COD_DO_MOVIMENTO"),
            "DATA_DE_MOVIMENTO": data.get("DATA_DE_MOVIMENTO"),
            "EMV_DO_QR_CODE": data.get("EMV_DO_QR_CODE"),
            "LOCATION": data.get("LOCATION"),
            "BRANCOS": data.get("BRANCOS"),
            "NUMERO_SEQUENCIAL": data.get("NUMERO_SEQUENCIAL"),
        }
        return dic_emv

    def trailer(self, data):
        dic_trailer = {
            "TIPO_DE_REGISTRO": data.get("TIPO_DE_REGISTRO"),
            "CODIGO_DE_RETORNO": data.get("CODIGO_DE_RETORNO"),
            "CODIGO_DO_SERVICO": data.get("CODIGO_DO_SERVICO"),
            "ISPB": data.get("ISPB"),
            "CODIGOS_DE_ERROR": data.get("CODIGOS_DE_ERROR"),
            "BRANCOS": data.get("BRANCOS"),
            "VALOR_TOTAL": data.get("VALOR_TOTAL"),
            "QTDE_DE_DETALHES": data.get("QTDE_DE_DETALHES"),
            "NUMERO_SEQUENCIAL": data.get("NUMERO_SEQUENCIAL"),
        }
        return dic_trailer
