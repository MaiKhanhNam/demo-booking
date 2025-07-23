# coding: utf8

from loguru import logger

from flask import Blueprint, jsonify
from app.routes.base import BaseRoute

import os

health_check_bp = Blueprint("health_check", __name__)


class HealthCheckRoute(BaseRoute):
    def __init__(self):
        super().__init__(health_check_bp)

    def register_routes(self):
        @self.blueprint.route("/ping", methods=["GET"])
        def health_check():
            return jsonify({"success": True, "data": "pong"})


HealthCheckRoute().register_routes()
