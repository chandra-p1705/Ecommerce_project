import os
import requests
from django.core.files.storage import Storage


class VercelBlobStorage(Storage):

    def _save(self, name, content):
        token = os.environ.get("BLOB_READ_WRITE_TOKEN")

        if not token:
            raise Exception("BLOB_READ_WRITE_TOKEN is missing")

        url = f"https://blob.vercel-storage.com/{name}"

        response = requests.put(
            url,
            data=content.read(),
            headers={
                "Authorization": f"Bearer {token}",
                "x-api-version": "4",
            },
        )

        if response.status_code not in [200, 201]:
            raise Exception(
                f"Vercel Blob upload failed: {response.status_code} {response.text}"
            )

        return name

    def _open(self, name, mode="rb"):
        raise NotImplementedError(
            "Files are stored in Vercel Blob."
        )

    def exists(self, name):
        return False

    def url(self, name):
        base_url = os.environ.get(
            "BLOB_BASE_URL",
            "https://voffn68xw0mkkon1.public.blob.vercel-storage.com"
        )
        return f"{base_url}/{name}"

    def delete(self, name):
        pass

    def size(self, name):
        return 0

