# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx

from pathlib_mate import PathCls as Path
from pylbd import service, path_object
from pylbd.service import Service, HOME, TMP, py_lbd_dirname


class TestServiceValidators(object):
    def test_check_service_name(self):
        def check_service_name(name):
            service.check_service_name(None, None, name)

        check_service_name("github_api")
        check_service_name("github-api")

    def test_check_project_dir(self):
        def check_project_dir(p):
            service.check_project_dir(None, None, p)

        # /project_dir/tests/test_service.py
        with raises(TypeError):
            check_project_dir(Path(__file__))

        # /project_dir/tests
        with raises(ValueError):
            check_project_dir(Path(__file__).parent)

        # /project_dir
        check_project_dir(Path(__file__).parent.parent)


    def test_check_root_workspace_dir(self):
        def check_root_workspace_dir(p):
            service.check_root_workspace_dir(None, None, p)

        check_root_workspace_dir(HOME)
        check_root_workspace_dir(TMP)


SERVICE_NAME = "my-service"
SERVICE_NAME_SLUG = "my-service"
SERVICE_VERSION = "0.0.1"
STAGE = "test"
AWS_ACCOUNT_ID = "111122223333"
AWS_ACCOUNT_ALIAS = "my-aws-account"


class TestServiceFileAndDirPath(object):
    service = Service(
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION,
        stage=STAGE,
        aws_account_id=AWS_ACCOUNT_ID,
        aws_account_alias=AWS_ACCOUNT_ALIAS,
        project_dir=Path(__file__).parent.parent,
        root_workspace_dir=HOME,
    )

    def test_build_lambda_dir(self):
        assert self.service.build_lambda_dir.abspath == Path(
            HOME, py_lbd_dirname, SERVICE_NAME, "build", "lambda"
        ).abspath

    def test_build_lambda_version_specified_dir(self):
        assert self.service.build_lambda_version_specified_dir.abspath == Path(
            HOME, py_lbd_dirname, SERVICE_NAME, "build", "lambda", SERVICE_VERSION
        ).abspath

    def test_deploy_pkg_zip(self):
        assert self.service.deploy_pkg_zip.abspath == Path(
            HOME, py_lbd_dirname, SERVICE_NAME, "build", "lambda", SERVICE_VERSION, "deploy-pkg.zip"
        ).abspath

    def test_source_zip(self):
        assert self.service.source_zip.abspath == Path(
            HOME, py_lbd_dirname, SERVICE_NAME, "build", "lambda", SERVICE_VERSION, "source.zip"
        ).abspath

    def test_layer_zip(self):
        assert self.service.layer_zip.abspath == Path(
            HOME, py_lbd_dirname, SERVICE_NAME, "build", "lambda", SERVICE_VERSION, "layer.zip"
        ).abspath

    def test_site_packages_dir(self):
        assert self.service.site_packages_dir.abspath == Path(
            HOME, py_lbd_dirname, SERVICE_NAME_SLUG, "build", "lambda", SERVICE_VERSION, "site-packages"
        ).abspath

    def test_s3_bucket_name(self):
        assert self.service.s3_bucket_name == "{}-{}-{}-deploy".format(
            AWS_ACCOUNT_ALIAS, SERVICE_NAME_SLUG, STAGE,
        )

    def test_deploy_pkg_source_layer_uri(self):
        bucket_name = "{}-{}-{}-deploy".format(
            AWS_ACCOUNT_ALIAS, SERVICE_NAME, STAGE,
        )
        assert self.service.deploy_pkg_s3_uri == "s3://{}/lambda/{}/{}/deploy-pkg.zip".format(
            bucket_name, SERVICE_NAME_SLUG, SERVICE_VERSION,
        )
        assert self.service.source_s3_uri == "s3://{}/lambda/{}/{}/source.zip".format(
            bucket_name, SERVICE_NAME_SLUG, SERVICE_VERSION,
        )
        assert self.service.layer_s3_uri == "s3://{}/lambda/{}/{}/layer.zip".format(
            bucket_name, SERVICE_NAME_SLUG, SERVICE_VERSION,
        )


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
