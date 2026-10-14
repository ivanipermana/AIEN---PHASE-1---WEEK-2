"""Lab S3 lokal. Jalankan dari folder paket: uv run python lab.py --help."""
import argparse
import csv
import io
import re
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError, EndpointConnectionError

ROOT = Path(__file__).resolve().parent
RAW_KEY = "raw/orders.csv"
RESULT_KEY = "processed/summary.csv"


def create_client():
    # Endpoint dan kredensial lab eksplisit, tidak memakai kredensial AWS pribadi.
    return boto3.client("s3", endpoint_url="http://127.0.0.1:4566",
                        region_name="us-east-1", aws_access_key_id="test",
                        aws_secret_access_key="test",
                        config=Config(s3={"addressing_style": "path"},
                                      connect_timeout=3, read_timeout=5,
                                      retries={"max_attempts": 1}))


def provision(s3, bucket):
    """TODO 1: buat bucket. Region lab us-east-1."""
    raise NotImplementedError("TODO 1: s3.create_bucket(Bucket=...)")


def upload(s3, bucket, path, key):
    """TODO 2: upload file lokal ke key yang diberikan."""
    raise NotImplementedError("TODO 2: s3.upload_file(Filename, Bucket, Key)")


def list_keys(s3, bucket):
    """TODO 3: gunakan list_objects_v2 dan kembalikan list key.
    Pagination sudah disediakan; lengkapi satu pemanggilan API.
    """
    keys, token = [], None
    while True:
        params = {"Bucket": bucket}
        if token:
            params["ContinuationToken"] = token
        response = None  # TODO 3: ganti dengan s3.list_objects_v2(**params)
        if response is None:
            raise NotImplementedError("TODO 3: list_objects_v2")
        keys.extend(obj["Key"] for obj in response.get("Contents", []))
        if not response.get("IsTruncated"):
            return sorted(keys)
        token = response["NextContinuationToken"]


def read_text(s3, bucket, key):
    """TODO 4: get_object lalu baca Body dan decode utf-8."""
    raise NotImplementedError("TODO 4: s3.get_object(Bucket=..., Key=...), lalu baca Body")


def aggregate(csv_text):
    """Sudah disediakan: seluruh nilai harga dan total adalah rupiah."""
    totals = defaultdict(lambda: {"orders": 0, "revenue": Decimal("0")})
    for row in csv.DictReader(io.StringIO(csv_text)):
        item = totals[row["category"]]
        item["orders"] += 1
        item["revenue"] += int(row["quantity"]) * Decimal(row["unit_price"])
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(["category", "order_count", "total_amount_idr"])
    for category, values in sorted(totals.items()):
        writer.writerow([category, values["orders"], f'{values["revenue"]:.0f}'])
    return output.getvalue()


def delete_one(s3, bucket, key):
    """TODO 5: hapus satu objek."""
    raise NotImplementedError("TODO 5: s3.delete_object(Bucket=..., Key=...)")


def delete_bucket(s3, bucket):
    """TODO 6: hapus bucket."""
    raise NotImplementedError("TODO 6: s3.delete_bucket(Bucket=...)")


def main():
    parser = argparse.ArgumentParser(description="Hands-on S3 lokal 60 menit")
    parser.add_argument("step", choices=["check", "provision", "ingest", "process", "inspect", "try-delete", "teardown"])
    parser.add_argument("--bucket", default="aien-orders-peserta")
    args = parser.parse_args()
    bucket = args.bucket
    if not re.fullmatch(r"aien-orders-[a-z0-9]+(?:-[a-z0-9]+)*", bucket) or len(bucket) > 63:
        parser.error("Gunakan nama aien-orders-<nama>, huruf kecil, angka, atau tanda minus; maks. 63 karakter.")
    s3 = create_client()
    if args.step == "check":
        s3.list_buckets()
        print("Koneksi S3 lokal berhasil.")
    elif args.step == "provision":
        provision(s3, bucket)
    elif args.step == "ingest":
        upload(s3, bucket, ROOT / "data/orders.csv", RAW_KEY)
        print("Objek:", list_keys(s3, bucket))
    elif args.step == "process":
        summary = aggregate(read_text(s3, bucket, RAW_KEY))
        path = ROOT / "hasil/summary.csv"
        path.parent.mkdir(exist_ok=True)
        path.write_text(summary, encoding="utf-8")
        upload(s3, bucket, path, RESULT_KEY)
        print(summary, end="")
    elif args.step == "inspect":
        print("Objek:", list_keys(s3, bucket))
        print(read_text(s3, bucket, RESULT_KEY), end="")
    elif args.step == "try-delete":
        keys = list_keys(s3, bucket)
        if not keys:
            raise RuntimeError("Bucket harus berisi objek untuk eksperimen. Jalankan ingest dahulu.")
        try:
            delete_bucket(s3, bucket)
        except ClientError as exc:
            if exc.response["Error"]["Code"] != "BucketNotEmpty":
                raise
            print("BucketNotEmpty: hapus objek dahulu sebelum menghapus bucket.")
        else:
            raise RuntimeError("Emulator menghapus bucket berisi data. Laporkan perbedaan perilaku ke instruktur.")
    elif args.step == "teardown":
        # Bucket lab tidak memakai versioning. Daftar seluruh key sebelum penghapusan.
        for key in list_keys(s3, bucket):
            delete_one(s3, bucket, key)
            print("Dihapus:", key)
        delete_bucket(s3, bucket)
        remaining = [b["Name"] for b in s3.list_buckets()["Buckets"]]
        if bucket in remaining:
            raise RuntimeError("Bucket masih ada.")
        print("Teardown berhasil: bucket sudah tidak ada.")


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError as exc:
        raise SystemExit(f"Lengkapi starter code: {exc}")
    except EndpointConnectionError:
        raise SystemExit("Floci belum terhubung. Periksa Docker Desktop, docker compose ps, dan port 4566.")
    except ClientError as exc:
        raise SystemExit(f'Error S3: {exc.response["Error"]["Code"]}. Periksa urutan langkah dan nama bucket.')
