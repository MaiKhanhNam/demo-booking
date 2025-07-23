# coding: utf8

def register_routes(app):
    from .health_check import health_check_bp
    from .booking import booking_bp

    app.register_blueprint(health_check_bp, url_prefix="/v1")
    app.register_blueprint(booking_bp, url_prefix="/v1/bookings")
