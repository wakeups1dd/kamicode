from app.services.sandbox.local_sandbox import LocalSandbox

def get_sandbox():
    """
    Factory function for sandbox. 
    In the future, this can check settings to return DockerSandbox or LocalSandbox.
    """
    return LocalSandbox()
