import os
import secrets

from flask import (
    render_template,
    request,
    send_file,
    abort,
    url_for,
    redirect
)

from flask_login import (
    login_required,
    current_user
)

from .database import db
from .models import File


def register_routes(app):

    BASE_DIR = os.path.abspath(os.getcwd())

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


    @app.route("/")
    def home():

        return render_template(
            "index.html",
            user=current_user
        )


    @app.route("/account")
    @login_required
    def account():

        return render_template(
            "account.html"
        )


    @app.route("/my-files")
    @login_required
    def my_files():

        files = File.query.filter_by(
            user_id=current_user.id
        ).order_by(
            File.uploaded_at.desc()
        ).all()

        return render_template(
            "my_files.html",
            files=files
        )


    @app.route("/upload", methods=["GET", "POST"])
    @login_required
    def upload():

        message = None
        share_url = None

        if request.method == "POST":

            uploaded = request.files.get("file")

            if uploaded and uploaded.filename:

                token = secrets.token_urlsafe(8)

                ext = os.path.splitext(uploaded.filename)[1]

                saved_name = token + ext

                save_path = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    saved_name
                )

                uploaded.save(save_path)

                record = File(
                    user_id=current_user.id,
                    token=token,
                    original_name=uploaded.filename,
                    saved_name=saved_name,
                    file_size=os.path.getsize(save_path)
                )

                db.session.add(record)
                db.session.commit()

                message = "تم رفع الملف بنجاح ✅"

                share_url = url_for(
                    "file_page",
                    token=token,
                    _external=True
                )

        return render_template(
            "upload.html",
            message=message,
            share_url=share_url
        )


    @app.route("/f/<token>")
    def file_page(token):

        file = File.query.filter_by(
            token=token
        ).first()

        if not file:
            abort(404)

        return render_template(
            "file.html",
            file=file
        )


    @app.route("/download/<token>")
    def download(token):

        file = File.query.filter_by(
            token=token
        ).first()

        if not file:
            abort(404)

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.saved_name
        )

        if not os.path.exists(filepath):
            abort(404)

        file.downloads += 1

        db.session.commit()

        return send_file(
            filepath,
            as_attachment=True,
            download_name=file.original_name
        )


    @app.route("/delete/<token>")
    @login_required
    def delete_file(token):

        file = File.query.filter_by(
            token=token,
            user_id=current_user.id
        ).first()

        if not file:
            abort(404)


        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.saved_name
        )


        if os.path.exists(filepath):
            os.remove(filepath)


        db.session.delete(file)

        db.session.commit()


        return redirect(
            url_for("my_files")
        )


    @app.route("/rename/<token>", methods=["POST"])
    @login_required
    def rename_file(token):

        file = File.query.filter_by(
            token=token,
            user_id=current_user.id
        ).first()

        if not file:
            abort(404)


        new_name = request.form.get(
            "name"
        ).strip()


        if new_name:

            file.original_name = new_name

            db.session.commit()


        return redirect(
            url_for("my_files")
        )
