from rest_framework import viewsets
import boto3
import json
import os
import asyncio
from botocore.exceptions import ClientError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class JSONFileView(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    class_serializer = None
    queryset = None

    def get(self, request):
        source_bucket_name = os.environ.get("AWS_STORAGE_BUCKET_NAME")
        destination_bucket_name = "citi-qr-response"

        loop = asyncio.new_event_loop()
        file_list = loop.run_until_complete(self.process_files(source_bucket_name, destination_bucket_name))
        loop.close()

        return Response(file_list)

    async def process_files(self, source_bucket_name, destination_bucket_name):
        s3 = boto3.resource('s3')
        source_bucket = s3.Bucket(source_bucket_name)
        destination_bucket = s3.Bucket(destination_bucket_name)
        file_list = []

        async def files(obj):
            if obj.key.endswith('.json'):
                file_data = obj.get()['Body'].read()
                file_data = file_data.decode('utf-8')
                file_data_json = json.loads(file_data)

                emv_value = file_data_json.get('EMV') if 'EMV' in file_data_json else None

                response_data = {
                    "data": [
                        {
                            "HEADER": file_data_json.get('HEADER'),
                            "DETALHE": file_data_json.get('DETALHE'),
                            "EMV": emv_value,
                            "TRAILER": file_data_json.get('TRAILER'),
                            "CODIGOS_DE_ERRO": file_data_json.get('CODIGOS_DE_ERROR')
                        }
                    ]
                }
                file_list.append(response_data)

                response_data_str = json.dumps(response_data)

                destination_file_name = f"{obj.key}"

                try:
                    destination_bucket.put_object(
                        Key=destination_file_name,
                        Body=response_data_str
                    )
                    # convert json to cnab750
                    # cnab750_data = self.convert_to_cnab750(response_data_str)
                    # print(cnab750_data)
                except ClientError as e:
                    print(f"Error uploading file {destination_file_name}: {e.response['Error']['Message']}")

        tasks = []
        for obj in source_bucket.objects.all():
            task = asyncio.ensure_future(files(obj))
            tasks.append(task)

        await asyncio.gather(*tasks)

        return file_list

    def convert_to_cnab750(self, data):
        # data = {
        #     "HEADER": {...},  # JSON data
        #     ...
        #         "CODIGOS_DE_ERROR": [...]  # JSON data
        # }

        cnab750_data = ""

        # Add HEADER data
        header_data = data["HEADER"]
        cnab750_data += "|".join(header_data.values()) + "\r\n"

        # Add DETALHE data
        detalhe_data = data["DETALHE"][0]
        cnab750_data += "|".join(detalhe_data.values()) + "\r\n"

        # Add REGISTRO_DETALHE_INFORMACOES_ADICIONAIS data
        informacoes_adicionais = detalhe_data["REGISTRO_DETALHE_INFORMACOES_ADICIONAIS"][0]
        cnab750_data += "|".join(informacoes_adicionais.values()) + "\r\n"

        # Add EMV data
        emv_data = data["EMV"]
        cnab750_data += "|".join(emv_data.values()) + "\r\n"

        # Add REGISTRO_DE_RECEBIMENTO data
        registro_recebimento = emv_data["REGISTRO_DE_RECEBIMENTO"][0]
        cnab750_data += "|".join(registro_recebimento.values()) + "\r\n"

        # Add TRAILER data
        trailer_data = data["TRAILER"]
        cnab750_data += "|".join(trailer_data.values()) + "\r\n"

        # Add CODIGOS_DE_ERROR data
        cnab750_data += "|".join(data["CODIGOS_DE_ERROR"]) + "\r\n"

        # Return the CNAB750 file as a response
        # response = HttpResponse(content_type="text/plain")
        # response["Content-Disposition"] = "attachment; filename=cnab750.rem"
        # response.write(cnab750_data)

        return cnab750_data
