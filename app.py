"""Flask app for adopt app."""

from flask import Flask, render_template, redirect

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


@app.get("/")
def display_home_page():
    """Presents the home page to the user"""

    pets = Pet.query.all()#TODO order by!

    return render_template(
        'home.html',
        pets=pets
    )

@app.route("/add", methods = ['GET','POST'])
def add_new_pet():
    """
        Either displays form to add a new pet, or submits the information
        and redirects to the homepage.

        TODO: reformat docstring:
        if GET then... show form

        if POST then...check valid then change db
    """

    form = AddPetForm()

    if form.validate_on_submit():

        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        new_pet = Pet(
            name=name,
            species=species,
            photo_url=photo_url,
            age=age,
            notes=notes,
        )

        db.session.add(new_pet)
        db.session.commit()
        return redirect("/")

    else:
        return render_template("pet_add_form.html", form=form)

@app.route("/<int:pet_id_number>", methods = ['GET','POST'])
def edit_pet_info(pet_id_number):
    """
        Render info page about given pet, and allow information updating.

        TODO: same here!
    """

    pet = Pet.query.get_or_404(pet_id_number)
    form = EditPetForm(
        photo_url = pet.photo_url,
        available = pet.available,
        notes = pet.notes #obj = pet here will do the same thing!! NOTE
    )

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data

        db.session.commit()

        return redirect(f'/{pet.id}')

    else:
        return render_template(
            "pet_display_info.html", #rename html TODO
            pet=pet,
            form=form
        )
