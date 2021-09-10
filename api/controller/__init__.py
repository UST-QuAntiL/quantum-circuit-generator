from api.controller import errors, encoding

MODULES = (
    encoding,
    errors,
)


def register_blueprints(api):
    """Initialize application with all modules"""
    for module in MODULES:
        api.register_blueprint(module.blp)
