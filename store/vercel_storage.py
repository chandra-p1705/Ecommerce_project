import os
from vercel.blob import put, del as delete_blob
from django.core.files.storage import Storage

class VercelBlobStorage(Storage):
    def _save(self, name, content):
        result = put(
            name,
            content.read(),
            {
                "access": "public",
            }
        )
        return result["url"]

    def _open(self, name, mode="rb"):
        raise NotImplementedError("Files are stored in Vercel Blob.")

    def exists(self, name):
        return False

    def url(self, name):
        return name

    def delete(self, name):
        delete_blob(name)

    def size(self, name):
        return 0