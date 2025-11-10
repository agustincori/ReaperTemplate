#push_bucket.py
import os
from google.cloud import storage


def upload_rpp_to_gcs(local_filename, bucket_name, destination_blob):
    """Uploads a file to a Google Cloud Storage bucket."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    blob.upload_from_filename(local_filename)
    print(f"✅ File '{local_filename}' uploaded to 'gs://{bucket_name}/{destination_blob}'.")


def find_rpp_file(root_dir="."):
    """Search recursively for the first .rpp file under root_dir."""
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".rpp"):
                return os.path.join(root, file)
    return None


def main():
    # 1. Find .rpp file recursively
    rpp_path = find_rpp_file(".")
    if not rpp_path:
        print("❌ No .rpp file found anywhere under this directory.")
        print(f"🔍 Current working directory: {os.getcwd()}")
        return

    # 2. Rename file to reaper_template.rpp in same folder
    new_path = os.path.join(os.path.dirname(rpp_path), "reaper_template.rpp")
    os.rename(rpp_path, new_path)
    print(f"📁 Renamed '{rpp_path}' → '{new_path}'")

    # 3. Upload to GCS
    bucket_name = "pacmaster-463402-storage"
    destination_path = "templates/reaper_template.rpp"
    upload_rpp_to_gcs(new_path, bucket_name, destination_path)


if __name__ == "__main__":
    main()
