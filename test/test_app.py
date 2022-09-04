#!/usr/bin/python3
import unittest
import json
import math

import requests

import common


class TestMathEndpoint(unittest.TestCase):

    def setUp(self) -> None:
        self.api_ip = common.get_api_ip()
        self.api_port = common.get_api_port()

    """Test the math endpoint of the API."""

    def test_circle_circumference(self):

        radius = 6.2
        url = f"http://{self.api_ip}:{self.api_port}/api/v1/math/circle/circumference"
        r = requests.get(
            url,
            data=json.dumps({"radius": radius}),
            headers={"Content-Type": "application/json"}
        )

        self.assertEqual(r.status_code, 200)
        circumference = r.json()
        self.assertEqual(circumference, math.pi*radius*2)

    def test_circle_radius(self):

        circumference = 5
        url = f"http://{self.api_ip}:{self.api_port}/api/v1/math/circle/radius"
        r = requests.get(
            url,
            data=json.dumps({"circumference": circumference}),
            headers={"Content-Type": "application/json"}
        )

        self.assertEqual(r.status_code, 200)
        radius = r.json()
        self.assertEqual(radius, circumference/2/math.pi)

    def test_triangle_area(self):

        height = 4
        base = 6
        url = f"http://{self.api_ip}:{self.api_port}/api/v1/math/triangle/area"
        r = requests.get(
            url,
            data=json.dumps({"height": height, "base": base}),
            headers={"Content-Type": "application/json"}
        )

        self.assertEqual(r.status_code, 200)
        area = r.json()
        self.assertEqual(area, height*base/2)


class TestVersionEndpoint(unittest.TestCase):

    def setUp(self) -> None:
        self.api_ip = common.get_api_ip()
        self.api_port = common.get_api_port()

    """Test the version endpoint of the API."""

    def test_v1(self):
        """Check that API servers version as a string with the form <major_version>.<minor_version> for version 1 requests"""

        url = f"http://{self.api_ip}:{self.api_port}/api/v1/version"
        r = requests.get(url, headers={"Version": "1"})

        self.assertEqual(r.status_code, 200)
        content = r.json()
        self.assertEqual(len(content.split(".")), 2)

    def test_v2(self):
        """Test that API serves version as a dict with keys 'major_version' and 'minor_version' for version 2 requests."""

        url = f"http://{self.api_ip}:{self.api_port}/api/v1/version"
        r = requests.get(url, headers={"Version": "2"})

        self.assertEqual(r.status_code, 200)
        content = r.json()
        self.assertTrue("major_version" in content)
        self.assertTrue("minor_version" in content)

    def test_v1_v2_equality(self):
        """Test that the API serves the same version for version 1 and 2 requests."""

        url = f"http://{self.api_ip}:{self.api_port}/api/v1/version"

        response_v1 = requests.get(url, headers={"Version": "1"})
        response_v2 = requests.get(url, headers={"Version": "2"})

        self.assertEqual(response_v1.status_code, 200)
        self.assertEqual(response_v2.status_code, 200)

        version_v1 = response_v1.json()

        content = response_v2.json()
        self.assertTrue("major_version" in content)
        self.assertTrue("minor_version" in content)

        version_v2 = f"{content['major_version']}.{content['minor_version']}"

        self.assertEqual(version_v1, version_v2)


if __name__ == "__main__":
    unittest.main()
