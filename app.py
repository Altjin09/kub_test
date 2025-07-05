from flask import Flask, render_template, request, redirect, url_for, session
import os

# --- OpenTelemetry imports ---
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# --- OpenTelemetry setup ---
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({
            "service.name": "kub_test"  # 👈 SigNoz дээр ингэж нэрлэгдэнэ
        })
    )
)
tracer = trace.get_tracer(__name__)  # ⬅️ Энэ мөрийг дээр нь гаргах хэрэгтэй

# OTEL_COLLECTOR_HOST-г орчноос унших буюу default-оор Docker host руу чиглүүлэх
otel_collector_host = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
exporter = OTLPSpanExporter(endpoint=otel_collector_host, insecure=True)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(exporter))

# --- Flask app setup ---
app = Flask(__name__)
app.secret_key = 'mysecretkey'

# OpenTelemetry Flask-д холбох
FlaskInstrumentor().instrument_app(app)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    with tracer.start_as_current_span("login-page"):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if username == 'admin' and password == 'password':
                session['user'] = username
                return redirect(url_for('dashboard'))
            else:
                return 'Нууц үг буруу байна'
        return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    with tracer.start_as_current_span("dashboard-page"):
        if 'user' not in session:
            return redirect(url_for('login'))
        port = request.environ.get('SERVER_PORT')
        return render_template('dashboard.html', port=port)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
