from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User model."""

    __tablename__ = 'users'

    user_id = db.Column(db.String(25), primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    mailing_address = db.Column(db.String(100),
                                default='383 Sutter St. San Francisco, CA',
                                nullable=False)
    firm_name = db.Column(db.String(64),
                          default='Wayne, Prince & Jones LLP',
                          nullable=False)

    def __repr__(self):
        """Provide info about the user instance."""

        return "<Name fname={} lname={}>".format(self.fname, self.lname)


class CaseUser(db.Model):
    """CaseUser model.

    An association of users to cases so that multiple users may work on a case."""

    __tablename__ = 'caseusers'

    team_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.String(25), db.ForeignKey('users.user_id'), nullable=False)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.case_id'), nullable=False)

    def __repr__(self):
        """Provide info about the CaseUser instance."""

        return "<CaseUser team_id={} user_id={} case_id={}>".format(self.team_id,
                                                                    self.user_id,
                                                                    self.case_id)


class Case(db.Model):
    """Case model."""

    __tablename__ = 'cases'

    case_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    case_no = db.Column(db.Integer, nullable=True)
    team_lead = db.Column(db.String(25), db.ForeignKey('users.user_id'), nullable=True)
    opposing_id = db.Column(db.Integer, db.ForeignKey('opposing_counsel.opposing_id'), nullable=True)
    claim_type_id = db.Column(db.Integer, db.ForeignKey('claim_types.claim_type_id'), nullable=True)
    damages_asked = db.Column(db.String(15), nullable=True)
    state = db.Column(db.String(25), nullable=True)
    county = db.Column(db.String(25), nullable=True)
    initialized = db.Column(db.DateTime, nullable=True)
    settlement_amount = db.Column(db.Integer, nullable=True)
    settled = db.Column(db.Boolean, default=False, nullable=False)

    # Define relationship to user
    users = db.relationship('User', secondary='caseusers', backref=db.backref('cases'))

    # Define relationship to parties
    parties = db.relationship('Party', secondary='caseparties', backref=db.backref('cases'))

    # Define relationship to plaintiffs
    plaintiff_join1 = "Case.case_id == CaseParty.case_id"
    plaintiff_join2 = "and_(CaseParty.party_id == Party.party_id, CaseParty.role_name == 'plaintiff')"

    plaintiffs = db.relationship("Party",
                                 primaryjoin=plaintiff_join1,
                                 secondary='caseparties',
                                 secondaryjoin=plaintiff_join2,
                                 backref=db.backref("cases_where_plaintiff"))

    # Define relationship to defendants
    defendant_join1 = "Case.case_id == CaseParty.case_id"
    defendant_join2 = "and_(CaseParty.party_id == Party.party_id, CaseParty.role_name == 'defendant')"

    defendants = db.relationship("Party",
                                 primaryjoin=defendant_join1,
                                 secondary='caseparties',
                                 secondaryjoin=defendant_join2,
                                 backref=db.backref("cases_where_defendant"))

    # Define relationship to cpmplaint
    complaint = db.relationship('Complaint', uselist=False, backref=db.backref('case'))
    # Define relationship to answer
    answer = db.relationship('Answer', uselist=False, backref=db.backref('case'))

    # Define relationship to opposing counsel
    opp = db.relationship('OpposingCounsel', backref=db.backref('cases'))

    def __repr__(self):
        """Provide info about the case instance."""

        return "<Case case_id={} initialized={}>".format(self.case_id,
                                                         self.initialized)

    def set_party_role(self, party, role):

        cp = CaseParty.query.filter(CaseParty.case_id == self.case_id,
                                    CaseParty.party_id == party.party_id).first()

        cp.role_name = role
        db.session.commit()


class CaseParty(db.Model):

    __tablename__ = 'caseparties'

    caseparty_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.party_id'), nullable=False)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.case_id'), nullable=False)
    role_name = db.Column(db.String(25), db.ForeignKey('roles.role_name'), nullable=True)


class Role(db.Model):
    """Role model: plaintiff or defendant."""

    __tablename__ = 'roles'

    role_name = db.Column(db.String(25), primary_key=True)


class Party(db.Model):
    """Party model."""

    __tablename__ = 'parties'

    party_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(25), nullable=True)
    lname = db.Column(db.String(25), nullable=True)
    company = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    residence = db.Column(db.String(100), nullable=True)


class OpposingCounsel(db.Model):
    """Opposition model."""

    __tablename__ = 'opposing_counsel'

    opposing_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    mailing_address = db.Column(db.String(100), nullable=True)
    firm_name = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide info about the opposing counsel instance."""

        return "<Name fname={} lname={}, from firm_name={}>".format(self.fname,
                                                                    self.lname,
                                                                    self.firm_name)


class DocType(db.Model):
    """Doctype model."""

    __tablename__ = 'doc_types'

    doc_type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide into about the document type."""

        return "<Document name={}>".format(self.name)


class ClaimType(db.Model):
    """Claim type model."""

    __tablename__ = 'claim_types'

    claim_type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide into about the claim type."""

        return "<Claim name={}>".format(self.name)


class Complaint(db.Model):
    """Complaint (document type) model."""

    __tablename__ = 'complaints'

    # Meta data on document
    complaint_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.case_id'), nullable=False)
    doc_type_id = db.Column(db.Integer, default=1, nullable=False)
    date_received = db.Column(db.DateTime, nullable=False)
    date_processed = db.Column(db.DateTime, nullable=True)
    # Substantive data from document - maybe include?
    # incident_date = db.Column(db.String(25), nullable=False)
    # incident_location = db.Column(db.String(100), nullable=False)
    # incident_description = db.Column(db.Text, nullable=False)
    damages_asked = db.Column(db.String(100), nullable=False)
    legal_basis = db.Column(db.String(64), nullable=True)
    # TODO: put on AWS and change to url
    pdf = db.Column(db.String(64), nullable=False)
    txt = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide into about the complaint instance."""

        return "<Complaint complaint_id={} case_id={}>".format(self.complaint_id,
                                                               self.case_id)


class Answer(db.Model):
    """Answer (document type) model."""

    __tablename__ = 'answers'

    answer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    doc_type_id = db.Column(db.Integer, default=2, nullable=False)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.case_id'), nullable=False)

    date_created = db.Column(db.DateTime, nullable=True)
    date_reviewed = db.Column(db.DateTime, nullable=True)
    date_submitted = db.Column(db.DateTime, nullable=True)

    docx = db.Column(db.String(64), nullable=False)  # will be url if online server or relative file /static/etc...

    def __repr__(self):
        """Provide into about the answer instance."""

        return "<Answer answer_id={} case_id={}>".format(self.answer_id,
                                                         self.case_id)


##############################################################################
# Helper functions

def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app, db_uri='postgres:///lglease'):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///lglease'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."