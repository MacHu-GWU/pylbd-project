# -*- coding: utf-8 -*-

import boto3
from botocore.exceptions import ClientError
import attr
from attrs_mate import AttrsClass
import weakref


@attr.s
class S3Object(AttrsClass):
    aws_profile = attr.ib()
    bucket = attr.ib() # type: str
    key = attr.ib() # type: str

    _s3_client_cache = weakref.WeakValueDictionary()

    def s3_client(self):
        if self.aws_profile not in self._s3_client_cache:
            client = boto3.session.Session(profile_name=self.aws_profile).client("s3")
            self._s3_client_cache[self.aws_profile] = client
        return self._s3_client_cache[self.aws_profile]

    def exists_on_s3(self):
        try:
            self.s3_client().head_object(Bucket=self.bucket, Key=self.key)
            return True
        except ClientError:
            return False
        except Exception as e:
            raise e

