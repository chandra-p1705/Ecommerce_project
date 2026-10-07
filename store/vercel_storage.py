import os
import requests
from urllib.parse import quote
from django.core.files.storage import Storage


class VercelBlobStorage(Storage):

    def _save(self, name, content):
        token = os.environ.get("BLOB_READ_WRITE_TOKEN")

        if not token:
            raise Exception("BLOB_READ_WRITE_TOKEN is missing")

        # pathname must be part of the URL, not a query parameter
        encoded_path = quote(name, safe="/")
        url = f"https://blob.vercel-storage.com/{encoded_path}"

        response = requests.put(
            url,
            data=content.read(),
            headers={
                "Authorization": f"Bearer {token}",
                "x-api-version": "7",
                "x-content-type": getattr(
                    content, "content_type", "application/octet-stream"
                ),
                "x-add-random-suffix": "0",
            },
        )

        if response.status_code not in (200, 201):
            raise Exception(
                f"Vercel Blob upload failed: "
                f"{response.status_code} {response.text}"
            )

        result = response.json()
        return result["url"]

    def _open(self, name, mode="rb"):
        raise NotImplementedError("Files are stored in Vercel Blob.")

    def exists(self, name):
        return False

    def url(self, name):
        if name.startswith("http://") or name.startswith("https://"):
            return name
        return "/" + name.lstrip("/")

    def delete(self, name):
        pass

    def size(self, name):
        return 0