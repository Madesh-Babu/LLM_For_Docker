from flask import Blueprint, request, jsonify
from src.service.rag_chain import run_rag

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat/inventory", methods=["POST"])
def chat_inventory():
    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({"error": "Missing 'question' field"}), 400

    question = data["question"]

    try:
        answer = run_rag(question)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
