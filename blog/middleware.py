import datetime

class RequestLogMiddleware:
    """
    Middleware que registra cada solicitud HTTP indicando:
    - ruta solicitada
    - método usado
    - fecha y hora

    Esto sirve para monitorear el tráfico de la aplicación.

    No cambia nada del sitio, sino que simplemente crea registros en cmd
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Registro de información
        method = request.method
        path = request.path
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"[{timestamp}] {method} request to {path}")

        # Continuar procesando
        response = self.get_response(request)
        return response