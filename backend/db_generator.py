"""
import backend.db_generator as model

model.artwork_db_generator(dbm.db.session, dbm.ArtworkModel)
model.user_db_generator(dbm.db.session, dbm.UserModel)
model.code_db_generator(dbm.db.session, dbm.InvitationCodeModel)
"""


def artwork_db_generator(db_session, artwork_model):
    """
    :param db_session: dbm.db.session
    :param artwork_model: dbm.ArtworkModel
    """

    db_session.add(
        artwork_model(
            artist="Vincent Van Gogh",
            created_date="1889",
            created_location="France",
            genre="post-impressionism",
            medium="oil painting",
            min_value=100000000,
            name="Starry Night",
            surface="canvas",
            width=921,
            height=737,
            seller=1,
        )
    )

    db_session.add(
        artwork_model(
            artist="Leonardo Da Vinci",
            created_date="1517",
            created_location="Louvre",
            genre="portrait",
            medium="oil painting",
            min_value=860000000,
            name="Mona Lisa",
            surface="poplar panel",
            width=530,
            height=770,
            seller=1,
        )
    )

    db_session.add(
        artwork_model(
            artist="Johannes Vermeer",
            created_date="1665",
            created_location="Netherlands",
            genre="portrait",
            medium="oil painting",
            min_value=30000000,
            name="Girl with a Pearl Earring",
            surface="canvas",
            width=390,
            height=445,
            seller=1,
        )
    )

    db_session.add(
        artwork_model(
            artist="Gustav Klimt",
            created_date="1908",
            created_location="Austria",
            genre="modern",
            medium="oil painting, pastels",
            min_value=240000,
            name="The Kiss",
            surface="canvas",
            width=1800,
            height=1800,
            seller=1,
        )
    )

    db_session.add(
        artwork_model(
            artist="Sandro Botticelli",
            created_date="1485",
            created_location="Italy",
            genre="renaissance",
            medium="oil painting, pastels",
            min_value=500000000,
            name="The Birth of Venus",
            surface="canvas",
            width=1725,
            height=2789,
            seller=1,
        )
    )

    db_session.add(
        artwork_model(
            artist="Peiter Bruegel the Elder",
            created_date="1565",
            created_location="Belgium",
            genre="renaissance",
            medium="oil painting",
            min_value=25000000,
            name="The Harvesters",
            surface="wood",
            width=1620,
            height=1190,
            seller=1,
        )
    )

    db_session.add(
        artwork_model(
            artist="Pablo Picasso",
            created_date="1937",
            created_location="France",
            genre="cubism",
            medium="oil painting",
            min_value=200000000,
            name="Guernica",
            surface="canvas",
            width=7766,
            height=3493,
            seller=1,
        )
    )

    db_session.add(
        artwork_model(
            artist="Francisco Goya",
            created_date="1800",
            created_location="Spain",
            genre="romanticism",
            medium="oil painting",
            min_value=10000000,
            name="The Naked Maja",
            surface="canvas",
            width=1900,
            height=970,
            seller=1,
        )
    )

    db_session.add(
        artwork_model(
            artist="Vincent Van Gogh",
            created_date="1890",
            created_location="France",
            genre="post-impressionism",
            medium="oil painting, graphite pencils",
            min_value=81300000,
            name="Almond Blossoms",
            surface="canvas",
            width=920,
            height=735,
            seller=1,
        )
    )

    db_session.add(
        artwork_model(
            artist="Georges Seurat",
            created_date="1886",
            created_location="France",
            genre="post-impressionism",
            medium="oil painting, graphite pencils",
            min_value=650000000,
            name="A Sunday Afternoon on the Island of La Grande Jatte",
            surface="canvas",
            width=3080,
            height=2076,
            seller=1,
        )
    )

    db_session.commit()


def user_db_generator(db_session, user_model):
    """
    :param db_session: dbm.db.session
    :param user_model: dbm.UserModel
    """

    db_session.add(
        user_model(
            email="dev01@artket.com",
            mobile="+13308575091",
            username="dev01",
            password="dev_pw_test",
        )
    )

    db_session.add(
        user_model(
            email="dev02@artket.com",
            mobile="+13308575092",
            username="dev02",
            password="dev_pw_test",
        )
    )

    db_session.commit()


def code_db_generator(db_session, code_model):
    """
    :param db_session: dbm.db.session
    :param code_model: dbm.InvitationCodeModel
    """
    import random
    import string

    def get_random_string(length):
        # choose from all lowercase letter
        letters = string.ascii_letters + string.digits + string.punctuation
        result_str = "".join(random.choice(letters) for _ in range(length))

        return str(result_str)

    print("checkpoint")
    for i in range(999):
        code = code_model(available_code=get_random_string(20))
        db_session.add(code)

    db_session.commit()
