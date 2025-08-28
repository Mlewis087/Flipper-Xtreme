"""Simple Flask web app exposing health insights."""
from __future__ import annotations

from typing import Dict

from flask import Flask, request, jsonify, render_template_string

from .main import gather_metrics
from .ai.analyzer import AIAnalyzer
from .subscription import SubscriptionService


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    subscriptions = SubscriptionService()
    # For demo purposes we give the default user an active subscription
    subscriptions.add_subscription("demo-user")

    form_html = """
    <h1>Health AI App</h1>
    <form method="post" action="/insights">
      <input name="user_id" placeholder="User ID" value="demo-user"/><br/>
      <input name="whoop_token" placeholder="Whoop token"/><br/>
      <input name="oura_token" placeholder="Oura token"/><br/>
      <input name="apple_token" placeholder="Apple token"/><br/>
      <button type="submit">Get Insights</button>
    </form>
    """

    @app.route("/")
    def index() -> str:
        return render_template_string(form_html)

    @app.route("/insights", methods=["POST"])
    def insights() -> tuple:
        user_id = request.form.get("user_id", "demo-user")
        if not subscriptions.is_active(user_id):
            return "Subscription inactive", 403
        tokens: Dict[str, str] = {
            "whoop": request.form.get("whoop_token", ""),
            "oura": request.form.get("oura_token", ""),
            "apple": request.form.get("apple_token", ""),
        }
        metrics = gather_metrics(tokens)
        analyzer = AIAnalyzer()
        feedback = analyzer.analyze(metrics)
        return jsonify({"metrics": metrics, "feedback": feedback})

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
