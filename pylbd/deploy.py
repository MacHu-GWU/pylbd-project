# -*- coding: utf-8 -*-

import attr
try:
    from .pkg.pathlib_mate import PathCls as Path
except:
    from pylbd.pkg.pathlib_mate import PathCls as Path

HOME = Path.home()


@attr.s
class Deployment(object):
    bucket_name = attr.ib()



@attr.s
class BuildFileManager(object):
    service_identifier = attr.ib()
    service_version = attr.ib()
    s3_bucket_name = attr.ib()
    s3_object_key_prefix = attr.ib()


    @property
    def _s3_object_key_prefix(self):
        if self.s3_object_key_prefix is None:
            return ""
        else:
            if self.s3_object_key_prefix.startswith("/"):
                self.s3_object_key_prefix = self.s3_object_key_prefix[1:]
            if self.s3_object_key_prefix.endswith("/"):
                self.s3_object_key_prefix = self.s3_object_key_prefix[:-1]
            return self.s3_object_key_prefix + "/"

    @property
    def s3_key_lambda_deploy_pkg(self):
        """
        The deployment package zip file S3 object key.
        """
        return "{_prefix}{service_identifier}/{service_version}/deploy_pkg.zip".format(
            _prefix=self._s3_object_key_prefix,
            service_identifier=self.service_identifier,
            service_version=self.service_version,
        )

    @property
    def s3_key_lambda_source(self):
        """
        The source code zip file S3 object key.
        """
        return "{_prefix}{service_identifier}/{service_version}/source.zip".format(
            _prefix=self._s3_object_key_prefix,
            service_identifier=self.service_identifier,
            service_version=self.service_version,
        )

    @property
    def s3_key_lambda_layer(self):
        """
        The lambda layer zip file S3 object key.
        """
        return "{_prefix}{service_identifier}/{service_version}/layer.zip".format(
            _prefix=self._s3_object_key_prefix,
            service_identifier=self.service_identifier,
            service_version=self.service_version,
        )

    path_build_dir = Path()

    @property
    def path_build_lambda_dir(self):
        return "${path_build_dir}/lambda"
    path_run_lambda_site_packages = "${path_build_dir}/lambda/site-packages"
    path_run_lambda_site_packages_service_library = "${path_run_lambda_site_packages}/${package_name}"



"${HOME}/${service_identifier}"