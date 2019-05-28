# -*- coding: utf-8 -*-

import pytest
from pylbd.s3_object import S3Object

class TestS3Object(object):
    def test(self):
        s3obj = S3Object(aws_profile="eqtest", bucket="eqtest-sanhe", key="hello.txt")
        assert s3obj.exists_on_s3() is True

        s3obj = S3Object(aws_profile="eqtest", bucket="eqtest-sanhe", key="file-not-exists.txt")
        assert s3obj.exists_on_s3() is False




if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
