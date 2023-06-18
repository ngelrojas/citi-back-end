from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError
from io import BytesIO

class JSONFileViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('boto3.resource')
    def test_get(self, mock_boto3_resource):
        source_bucket_name = "citi-qr-code"
        destination_bucket_name = "citi-qr-response"
        mock_s3 = mock_boto3_resource.return_value
        mock_source_bucket = MagicMock()
        mock_destination_bucket = MagicMock()
        mock_s3.Bucket.side_effect = [mock_source_bucket, mock_destination_bucket]

        # Mock the objects in the source bucket
        mock_objects = [
            MagicMock(key='file1.json', get=lambda: {'Body': BytesIO(b'{"HEADER": "header1", "DETALHE": "detalhe1", "EMV": "emv1", "TRAILER": "trailer1", "CODIGOS_DE_ERRO": "error1"}')}),
            MagicMock(key='file2.json', get=lambda: {'Body': BytesIO(b'{"HEADER": "header2", "DETALHE": "detalhe2", "TRAILER": "trailer2", "CODIGOS_DE_ERRO": "error2"}')}),
            MagicMock(key='file3.txt', get=lambda: {'Body': BytesIO(b'text file')}),
        ]
        mock_source_bucket.objects.all.return_value = mock_objects

        response = self.client.get('/json-files/')

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Assert file list in the response
        expected_response_data = [
            {
                "data": [
                    {
                        "HEADER": "header1",
                        "DETALHE": "detalhe1",
                        "EMV": "emv1",
                        "TRAILER": "trailer1",
                        "CODIGOS_DE_ERRO": "error1"
                    }
                ]
            },
            {
                "data": [
                    {
                        "HEADER": "header2",
                        "DETALHE": "detalhe2",
                        "EMV": None,
                        "TRAILER": "trailer2",
                        "CODIGOS_DE_ERRO": "error2"
                    }
                ]
            }
        ]
        self.assertEqual(response.json(), expected_response_data)

        # Assert that the files were uploaded to the destination bucket
        expected_destination_calls = [
            MagicMock(Key='file1.json', Body='{"data": [{"HEADER": "header1", "DETALHE": "detalhe1", "EMV": "emv1", "TRAILER": "trailer1", "CODIGOS_DE_ERRO": "error1"}]}'),
            MagicMock(Key='file2.json', Body='{"data": [{"HEADER": "header2", "DETALHE": "detalhe2", "EMV": null, "TRAILER": "trailer2", "CODIGOS_DE_ERRO": "error2"}]}'),
        ]
        mock_destination_bucket.put_object.assert_has_calls(expected_destination_calls)

        # Assert that the mock source bucket and destination bucket were accessed
        mock_s3.Bucket.assert_any_call(source_bucket_name)
        mock_s3.Bucket.assert_any_call(destination_bucket_name)

    @patch('boto3.resource')
    def test_get_with_upload_error(self, mock_boto3_resource):
        source_bucket_name = "citi-qr-code"
        destination_bucket_name = "citi-qr-response"
        mock_s3 = mock_boto3_resource.return_value
        mock_source_bucket = MagicMock()
        mock_destination_bucket = MagicMock()
        mock_s3.Bucket.side_effect = [mock_source_bucket, mock_destination_bucket]

        # Mock the objects in the source bucket
        mock_objects = [
            MagicMock(key='file1.json', get=lambda: {'Body': BytesIO(b'{"HEADER": "header1", "DETALHE": "detalhe1", "EMV": "emv1", "TRAILER": "trailer1", "CODIGOS_DE_ERRO": "error1"}')}),
        ]
        mock_source_bucket.objects.all.return_value = mock_objects

        # Raise an error when trying to upload the file
        mock_destination_bucket.put_object.side_effect = ClientError({'Error': {'Message': 'Upload error'}}, 'put_object')

        response = self.client.get('/json-files')

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Assert file list in the response (should still contain the file)
        expected_response_data = [
            {
                "data": [
                    {
                        "HEADER": "header1",
                        "DETALHE": "detalhe1",
                        "EMV": "emv1",
                        "TRAILER": "trailer1",
                        "CODIGOS_DE_ERRO": "error1"
                    }
                ]
            }
        ]
        self.assertEqual(response.json(), expected_response_data)

        # Assert that the file upload error was logged
        mock_destination_bucket.put_object.assert_called_once()

        # Assert that the mock source bucket and destination bucket were accessed
        mock_s3.Bucket.assert_any_call(source_bucket_name)
        mock_s3.Bucket.assert_any_call(destination_bucket_name)
