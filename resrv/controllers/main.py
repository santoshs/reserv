from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import and_

from resrv.forms import LoginForm, MachineAddForm, UserForm
from resrv.models import db, User, Machine, ReservationHistory

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template('index.html')

@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user)

        flash("Logged in successfully.", "info")
        return redirect(request.args.get("next") or url_for(".home"))

    return render_template("login.html", form=form)


@main.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for(".home"))

@main.route("/me", defaults={"id": None})
@main.route("/profile/<id>")
def profile(id):
    if not id:
        if current_user.is_authenticated:
            id = current_user.id
        else:
            return None, 404
    user = User.query.get(id)
    return render_template("profile.html", user=user)

@main.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = UserForm(obj=current_user)
    if form.validate_on_submit():
        if form.email.data:
            current_user.email = form.email.data
        if form.password.data:
            current_user.set_password(form.password.data)

        db.session.add(current_user)
        db.session.commit()
        flash("Profile Updated", "info")
        return redirect(url_for(".home"))

    for field, errors in form.errors.items():
        for error in errors:
            flash(error, 'warning')

    return render_template("edit_profile.html", form=form)

@main.route("/add_machine", defaults={"id": None}, methods=["GET", "POST"])
@main.route("/add_machine/<id>", methods=["GET", "POST"])
@login_required
def add_machine(id):
    m = Machine.query.get(id)
    form = MachineAddForm(obj=m)

    if form.validate_on_submit():
        if m is None:
            flash("Machine details added successfully.", "info")
            m = Machine(form.hostname.data, form.address.data, form.alias.data)
        else:
            form.populate_obj(m)
            flash("Machine details updated.", "info")

        db.session.add(m)
        db.session.commit()
        return redirect(url_for(".machine", id=m.id))

    for field, errors in form.errors.items():
        for error in errors:
            flash(error, 'warning')

    return render_template("add_machine.html", form=form, machine=m)


@main.route("/machine/<id>")
def machine(id):
    machine = Machine.query.get(id)
    if machine is None:
        flash("No such machine, select one from the machine list", "warning")
        return redirect(url_for(".machine_list"))

    return render_template("machine.html", machine=machine)

@main.route("/machines")
def machine_list():
    machines = Machine.query.all()
    return render_template('machine_list.html', machines=machines)

@main.route("/reserve/<id>")
@login_required
def reserve(id):
    m = Machine.query.get(id)

    if m is None:
        flash("No such machine, select one from the machine list", "warning")
        return redirect(url_for(".machine_list"))

    if len(m.reservation) > 0:
        if m.reservation[0].id == current_user.id:
            user = "you"
        else:
            user = "@" + m.reservation[0].username
        flash("Machine is already reserved by {}".format(user), "warning");
    else:
        db.session.add(ReservationHistory(id, current_user.id))
        m.reservation.append(current_user)
        db.session.commit()
        flash("@{}, Machine successfully reserved!".format(current_user.username), "info")

    return redirect(url_for(".machine", id=id))

@main.route("/release/<id>")
@login_required
def release(id):
    if len(current_user.reserved_machines) == 0:
        flash("You don't have any machines reserved", "warning")
        return redirect(url_for(".machine", id=id))

    m = Machine.query.get(id)
    if len(m.reservation) == 0:
        flash("Machine not reserved yet", "warning")
        return redirect(url_for(".machine", id=id))

    if len(m.reservation) > 1:
        flash("MultipleReservations: Internal error", "danger")
        return redirect(url_for(".machine", id=id))

    if m in current_user.reserved_machines:
        current_user.reserved_machines.remove(m)
        db.session.commit()
        flash("Machine {} released".format(m.alias), "info")
        return redirect(url_for(".machine_list", id=id))
    else:
        flash("Machine is not reserved by you", "danger")
        return redirect(url_for(".machine", id=id))


@main.route("/sysacces/<id>")
def sys_access(id):
    m = Machine.query.get(id)

    if not m:
        return None, 404

    return render_template("sys_access.dat", machine=m)
