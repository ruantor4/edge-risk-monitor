import requests

def authenticate(api_base_url: str, username: str, password: str) -> str:
    """
    Realiza autenticação na API externa de monitoramento.

    Esta função executa o processo de login na API Edge Monitor,
    enviando credenciais de acesso e retornando um token JWT
    utilizado para autenticação das requisições subsequentes.

    Parameters
    ----------
    api_base_url : str
        URL base da API de monitoramento.
    username : str
        Nome de usuário utilizado para autenticação.
    password : str
        Senha associada ao usuário informado.

    Returns
    -------
    str
        Token de acesso JWT retornado pela API.
    """
    response = requests.post(
        f"{api_base_url}/api/authentication/login/",
        json={
            "username": username,
            "password": password,
        },
        timeout=10,
    )

    response.raise_for_status()
    return response.json()["access"]