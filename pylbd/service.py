# -*- coding: utf-8 -*-

"""

- Each Micro Service should have its own Stack. same micro service in different stage should have isolated environment.
"""

import attr
import string
from .pkg.pathlib_mate import PathCls as Path
from .pkg.sfm.rnd import rand_hexstr


HOME = Path.home()
TMP = Path("/tmp")

py_lbd_dirname = "pylbd"

def check_project_dir(instance, attribute, value):
    if not value.is_dir():
        raise TypeError("project_dir has to be a directory")

    p = Path(value, "setup.py")
    if not p.exists():
        raise ValueError("'%s' doesn't exists!" % p)

    p = Path(value, "serverless.yml")
    if not p.exists():
        raise ValueError("'%s' doesn't exists!" % p)


def check_root_workspace_dir(instance, attribute, value):
    if not value.exists():
        raise ValueError("'%s' doesn't exists!" % value)

    try:
        basename = "pylbd-test-{}.txt".format(rand_hexstr(6))
        p = Path(value, basename)
        p.write_text("test ...", encoding="utf-8")
        p.read_text(encoding="utf-8")
        p.remove()
    except Exception as e:
        raise EnvironmentError("Unable to read and write a test file in %s: %s" % (value, e))


def check_service_name(instance, attribute, value):
    if value[0] not in string.ascii_letters:
        raise ValueError("'service_name' has to be start with ascii letters!")


def check_stage(instance, attribute, value):
    valid_stages = {
        Stage.dev, Stage.test, Stage.stage, Stage.qa, Stage.prod,
    }
    if value not in valid_stages:
        raise ValueError("stage has to be one of %s" % valid_stages)


class Stage:
    dev = "dev"
    test = "test"
    stage = "stage"
    qa = "qa"
    prod = "prod"


@attr.s
class Service(object):
    """

    ::

        <root_workspace>
            |-- pylbd
                |-- <service_name>
                    |-- build
                        |-- lambda
                            |-- <service_version>
                                |-- deploy-pkg.zip
                                |-- source.zip
                                |-- layer.zip

    ::

        <project_dir>
        |-- bin
            |-- lbd
        |-- <package_name> (usually same as service_name)
            |--
        |-- build
            |-- config.json
            |-- config-dev/test/stage/prod.json
        |-- serverless.yml

    """
    service_name = attr.ib() # type: str
    service_version = attr.ib()  # type: str
    stage = attr.ib(validator=check_stage) # type: str

    aws_account_id = attr.ib()  # type: str
    aws_account_alias = attr.ib()  # type: str

    project_dir = attr.ib(validator=check_project_dir) # type: Path
    root_workspace_dir = attr.ib(default=HOME, validator=check_root_workspace_dir) # type: Path

    @property
    def service_name_slug(self):
        return self.service_name.replace("_", "-")

    @property
    def build_lambda_dir(self):
        return Path(self.root_workspace_dir, py_lbd_dirname, self.service_name_slug, "build", "lambda")

    @property
    def build_lambda_version_specified_dir(self):
        return Path(self.build_lambda_dir, self.service_version)

    @property
    def deploy_pkg_zip(self):
        """
        The full deployment package includes the source code and dependencies
        layer. If you use layer, most likely you don't need this.
        """
        return Path(self.build_lambda_version_specified_dir, "deploy-pkg.zip")

    @property
    def source_zip(self):
        """
        Everything in the package source code.
        """
        return Path(self.build_lambda_version_specified_dir, "source.zip")

    @property
    def layer_zip(self):
        """
        The Lambda Layer includes all python library dependencies, usually it
        is corresponding to the requirements.txt file. Except AWS Lambda Python
        runtime built-in library:

        - botocore/
        - boto3/
        - s3transfer/

        And should exclude system related python library:

        - setuptools/
        - pip/
        - easy_install.py
        - wheel/
        - twine/
        - _pytest/
        - pytest/

        And the service package it self:

        - <package_name>/
        """
        return Path(self.build_lambda_version_specified_dir, "layer.zip")

    @property
    def site_packages_dir(self):
        """
        Everything
        """
        return Path(self.build_lambda_version_specified_dir, "site-packages")

    @property
    def s3_bucket_name(self):
        """
        The S3 bucket used for deployment.

        Example: ``my-aws-account-alias-my-service-test``
        """
        return "{aws_account_alias}-{service_name_slug}-{stage}-deploy".format(
            aws_account_alias=self.aws_account_alias,
            service_name_slug=self.service_name_slug,
            stage=self.stage,
        )

    @property
    def build_lambda_version_specified_s3_key(self):
        """
        The S3 key or the directory that
        stores the all kinds of deployment package zip files.

        Example:: ``lambda/my-service/0.0.1``
        """
        return "lambda/{service_name_slug}/{service_version}".format(
            service_name_slug=self.service_name_slug,
            service_version=self.service_version,
        )

    @property
    def deploy_pkg_s3_key(self):
        """
        The local deploy-pkg.zip file will be uploaded to s3 at here.
        It is only the S3 key part (no bucket information).
        """
        return "{}/deploy-pkg.zip".format(self.build_lambda_version_specified_s3_key)

    @property
    def source_s3_key(self):
        return "{}/source.zip".format(self.build_lambda_version_specified_s3_key)

    @property
    def layer_s3_key(self):
        return "{}/layer.zip".format(self.build_lambda_version_specified_s3_key)

    @property
    def deploy_pkg_s3_uri(self):
        """
        The local deploy-pkg.zip file will be uploaded to s3 at here.
        It is the full S3 URI of the object.
        """
        return "s3://{}/{}".format(self.s3_bucket_name, self.deploy_pkg_s3_key)

    @property
    def source_s3_uri(self):
        return "s3://{}/{}".format(self.s3_bucket_name, self.source_s3_key)

    @property
    def layer_s3_uri(self):
        return "s3://{}/{}".format(self.s3_bucket_name, self.layer_s3_key)
