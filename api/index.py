"""
Safe serverless entrypoint.

Importing the full Flask `app` can raise at runtime in serverless environments
and cause the function to crash. Import lazily and provide a minimal fallback
Flask app that returns an informative error (so the function never fails
silently). This keeps Vercel from showing a generic "FUNCTION_INVOCATION_FAILED"
message and surfaces the real import error in the response and logs.
"""
import traceback

try:
	from app import app
except Exception as _import_err:
	# Create a tiny fallback Flask app that reports the import error
	from flask import Flask, jsonify

	fallback = Flask(__name__)

	@fallback.route("/", defaults={"path": ""})
	@fallback.route("/<path:path>")
	def _import_error(path):
		tb = traceback.format_exc()
		# Keep the response compact but include the traceback for debugging logs
		return (
			jsonify({
				"error": "import_failed",
				"message": str(_import_err),
				"traceback": tb.splitlines()[-10:],
			}),
			500,
		)

	app = fallback
