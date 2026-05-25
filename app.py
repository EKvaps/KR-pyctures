from flask import Flask, request, redirect, session

app = Flask(__name__)
app.secret_key = "kr_pyctures_secret"

PASSWORD = "user0000"
GANANCIA = 60

productos = []


@app.route("/", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        password = request.form.get("password")

        if password == PASSWORD:
            session["login"] = True
            return redirect("/loading")
        else:
            error = "Contraseña incorrecta"

    return f"""
    <html>
    <head>
        <title>Login</title>
        <style>
            body {{
                background: #111;
                color: white;
                font-family: Arial;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}

            .box {{
                background: #1e1e1e;
                padding: 40px;
                border-radius: 20px;
                text-align: center;
                width: 300px;
                box-shadow: 0px 0px 20px rgba(0,0,0,0.5);
            }}

            input {{
                width: 100%;
                padding: 12px;
                margin-top: 15px;
                border: none;
                border-radius: 10px;
            }}

            button {{
                margin-top: 20px;
                padding: 12px;
                width: 100%;
                border: none;
                border-radius: 10px;
                background: #00b894;
                color: white;
                font-size: 16px;
                cursor: pointer;
            }}

            h1 {{
                color: #00ff99;
            }}
        </style>
    </head>

    <body>
        <div class='box'>
            <h1>KR Control</h1>
            <form method='POST'>
                <input type='password' name='password' placeholder='Contraseña'>
                <button type='submit'>Entrar</button>
            </form>
            <p style='color:red'>{error}</p>
        </div>
    </body>
    </html>
    """


@app.route("/loading")
def loading():
    if not session.get("login"):
        return redirect("/")

    return """
    <html>
    <head>
        <meta http-equiv="refresh" content="3;url=/panel">

        <style>
            body {
                background: #111;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                flex-direction: column;
                font-family: Arial;
            }

            .loader {
                border: 10px solid #333;
                border-top: 10px solid #00ff99;
                border-radius: 50%;
                width: 100px;
                height: 100px;
                animation: spin 1s linear infinite;
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }

            h1 {
                margin-top: 30px;
            }
        </style>
    </head>

    <body>
        <div class='loader'></div>
        <h1>Cargando datos...</h1>
    </body>
    </html>
    """


@app.route("/panel", methods=["GET", "POST"])
def panel():
    if not session.get("login"):
        return redirect("/")

    mensaje = ""

    if request.method == "POST":

        if "agregar" in request.form:
            nombre = request.form.get("nombre")
            costo = float(request.form.get("costo"))

            venta = costo + (costo * GANANCIA / 100)

            productos.append({
                "nombre": nombre,
                "costo": costo,
                "venta": venta
            })

            mensaje = "Producto agregado"

        if "eliminar" in request.form:
            index = int(request.form.get("index"))

            if 0 <= index < len(productos):
                productos.pop(index)
                mensaje = "Producto eliminado"

    filas = ""

    for i, producto in enumerate(productos):
        filas += f"""
        <tr>
            <td>{producto['nombre']}</td>
            <td>${producto['costo']:,.0f}</td>
            <td>{GANANCIA}%</td>
            <td>${producto['venta']:,.0f}</td>
            <td>
                <form method='POST'>
                    <input type='hidden' name='index' value='{i}'>
                    <button name='eliminar'>Eliminar</button>
                </form>
            </td>
        </tr>
        """

    return f"""
    <html>
    <head>
        <title>KR Control</title>

        <style>
            body {{
                background: #121212;
                color: white;
                font-family: Arial;
                padding: 30px;
            }}

            h1 {{
                color: #00ff99;
                text-align: center;
            }}

            .bienvenida {{
                text-align: center;
                font-size: 20px;
                margin-bottom: 30px;
            }}

            .box {{
                background: #1e1e1e;
                padding: 20px;
                border-radius: 20px;
                margin-bottom: 20px;
            }}

            input {{
                padding: 12px;
                margin: 5px;
                border: none;
                border-radius: 10px;
            }}

            button {{
                padding: 12px 20px;
                border: none;
                border-radius: 10px;
                background: #00b894;
                color: white;
                cursor: pointer;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}

            th, td {{
                border: 1px solid #333;
                padding: 15px;
                text-align: center;
            }}

            th {{
                background: #222;
            }}
        </style>
    </head>

    <body>

        <h1>KR Control de Productos</h1>

        <div class='bienvenida'>
            Bienvenido Esteban
        </div>

        <div class='box'>
            <form method='POST'>
                <input type='text' name='nombre' placeholder='Nombre producto' required>
                <input type='number' name='costo' placeholder='Costo producto' required>
                <button name='agregar'>Agregar Producto</button>
            </form>
        </div>

        <p>{mensaje}</p>

        <table>
            <tr>
                <th>Producto</th>
                <th>Costo</th>
                <th>Ganancia</th>
                <th>Venta</th>
                <th>Acción</th>
            </tr>

            {filas}

        </table>

    </body>
    </html>
    """


if __name__ == "__main__":
   import os

app.run(
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 10000))
)
