# Simple Storage

File storage made simple.

[![codecov](https://codecov.io/gh/merixstudio/simple-storage/branch/master/graph/badge.svg?token=XMH3S6M34G)](https://codecov.io/gh/merixstudio/simple-storage)

![python](https://img.shields.io/badge/Python-3.6%2B-brightgreen)

## Supported storages

- File system
- AWS S3

## Requirements

- Python >= 3.6

# How to use

Install the package:

```shell
pip install simple-storage
```

Now, depending on the storage you want to use, follow the instructions below.

## File system storage

| Environment variable | Value                                                               |
|----------------------|---------------------------------------------------------------------|
| `STORAGES_BACKEND`   | `storages.backends.file_system.FileSystemStorage`                   |
| `STORAGES_PATH`      | Point to the existing path in your file system, e.g.  `/app/media`. |

## AWS S3 storage

| Environment variable             | Value                                         |
|----------------------------------|-----------------------------------------------|
| `STORAGES_BACKEND`               | `storages.backends.amazon_s3.AmazonS3Storage` |
| `STORAGES_AWS_ACCESS_KEY_ID`     | Your AWS access key ID.                       |
| `STORAGES_AWS_SECRET_ACCESS_KEY` | Your AWS secret access key.                   |
| `STORAGES_BUCKET_NAME`           | The bucket name that you want to use.         |

> In case you encounter any problems with finding your AWS credentials please read [this page][1] as a reference.

[1]: https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html "Understanding and getting your AWS credentials"
